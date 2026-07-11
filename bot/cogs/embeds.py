import discord
from discord import app_commands
from discord.ext import commands

from config import BRAND_COLOR, STUDIO_NAME, BANNERS, branded_embed, panel


class EmbedBuilder(discord.ui.Modal, title="Create a Custom Embed"):
    """A pop-up form that lets staff build a custom embed live."""

    e_title = discord.ui.TextInput(label="Title", required=False, max_length=256)
    e_desc = discord.ui.TextInput(label="Description", style=discord.TextStyle.paragraph,
                                  required=False, max_length=2000)
    e_color = discord.ui.TextInput(label="Color hex (e.g. #1e9bff)", required=False, max_length=7)
    e_image = discord.ui.TextInput(label="Image URL (optional)", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            color = discord.Color.from_str(self.e_color.value) if self.e_color.value else BRAND_COLOR
        except ValueError:
            color = BRAND_COLOR
        embed = discord.Embed(title=self.e_title.value or None,
                              description=self.e_desc.value or None, color=color)
        if self.e_image.value:
            embed.set_image(url=self.e_image.value)
        embed.set_footer(text=STUDIO_NAME)
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Embed posted!", ephemeral=True)


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Build and post a custom embed (staff only).")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def embed(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EmbedBuilder())

    @app_commands.command(description="Show info about this server.")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild

        embed = branded_embed(title=g.name, description=g.description or "Server information")
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)

        embed.add_field(name="Members", value=g.member_count, inline=True)
        embed.add_field(name="Channels", value=len(g.channels), inline=True)
        embed.add_field(name="Roles", value=len(g.roles), inline=True)
        embed.add_field(name="Owner", value=g.owner.mention if g.owner else "Unknown", inline=True)
        embed.add_field(name="Created", value=g.created_at.strftime("%b %d, %Y"), inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Post a branded announcement panel.")
    @app_commands.describe(title="Panel title", message="What it should say")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def announce(self, interaction: discord.Interaction, title: str, message: str):
        await interaction.channel.send(embeds=panel(title, message, banner=BANNERS["welcome"]))
        await interaction.response.send_message("Posted!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Embeds(bot))
