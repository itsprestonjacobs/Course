import io
import os

import discord
from discord import app_commands
from discord.ext import commands

from config import BRAND_COLOR, STUDIO_NAME, BANNERS, branded_embed, panel

STAFF_ROLE_NAME = os.getenv("STAFF_ROLE_NAME", "Staff")

# The choices in the dropdown. (label, description, emoji) — add or remove
# rows to change what people can open a ticket for.
CATEGORIES = [
    ("General Support", "Questions, feedback, or anything else", "💬"),
    ("Payment / Refund", "Billing and refund help", "💳"),
    ("Partnership", "Partnership and event requests", "🤝"),
]


async def create_ticket(interaction: discord.Interaction, category: str):
    guild = interaction.guild
    author = interaction.user

    # One open ticket per person.
    existing = discord.utils.get(guild.text_channels, name=f"ticket-{author.id}")
    if existing:
        await interaction.response.send_message(
            f"You already have a ticket open: {existing.mention}", ephemeral=True)
        return

    staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)

    # Hide the channel from everyone, then let the author, staff, and the bot in.
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
    }
    if staff_role:
        overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

    channel = await guild.create_text_channel(
        name=f"ticket-{author.id}",
        overwrites=overwrites,
        topic=f"{category} ticket for {author} ({author.id})",
    )

    embed = branded_embed(
        title=f"{category} ticket",
        description=f"Hey {author.mention}, thanks for reaching out. A staff member will be "
                    "with you shortly.\nUse the button below when you're done.",
    )
    await channel.send(content=author.mention, embed=embed, view=CloseTicket())
    await interaction.response.send_message(f"Your ticket is ready: {channel.mention}", ephemeral=True)


class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=label, description=desc, emoji=emoji)
            for label, desc, emoji in CATEGORIES
        ]
        super().__init__(
            placeholder="Select what you need help with…",
            options=options,
            custom_id="ticket:open",
        )

    async def callback(self, interaction: discord.Interaction):
        await create_ticket(interaction, self.values[0])


class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())


class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red,
                       emoji="🔒", custom_id="ticket:close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        await interaction.response.send_message("Saving transcript and closing…")

        # Save a plain-text transcript so there's a record after the channel is gone.
        lines = []
        async for message in channel.history(limit=None, oldest_first=True):
            stamp = message.created_at.strftime("%Y-%m-%d %H:%M")
            lines.append(f"[{stamp}] {message.author}: {message.content}")
        transcript = "\n".join(lines) or "(no messages)"

        log_channel = discord.utils.get(interaction.guild.text_channels, name="ticket-logs")
        if log_channel:
            file = discord.File(io.BytesIO(transcript.encode()), filename=f"{channel.name}.txt")
            await log_channel.send(f"Transcript for `{channel.name}`", file=file)

        await channel.delete()


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        # Re-register the views on startup so old panels keep working after a restart.
        self.bot.add_view(TicketPanel())
        self.bot.add_view(CloseTicket())

    @app_commands.command(description="Post the ticket panel in this channel (staff only).")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def ticketpanel(self, interaction: discord.Interaction):
        embeds = panel(
            title="🎫 | Support",
            description="Need a hand? Pick an option from the dropdown below to open a "
                        "private ticket and our team will help you out.",
            banner=BANNERS["assistance"],
        )
        await interaction.channel.send(embeds=embeds, view=TicketPanel())
        await interaction.response.send_message("Panel posted!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Tickets(bot))
