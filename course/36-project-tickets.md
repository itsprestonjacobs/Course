# Project: Ticket System

Time to put it all together. The ticket system uses almost everything you've learned:
embeds, dropdowns, permissions, private channels, persistence, and files. It's the same kind
of support panel the Derpy's Designs server runs. We'll build it in small, testable pieces.

## What we're building

A branded panel with a **dropdown**. When a member picks a category, the bot creates a
**private channel** only they and staff can see, with a **Close** button that saves a
**transcript** and deletes the channel — and it all survives a bot restart.

## Step 0 — Server prep

In your test server, create:
- a **role** named `Staff` (it will see tickets),
- optionally a channel named `ticket-logs` (transcripts land here).

## Step 1 — The cog + categories

Make `cogs/tickets.py`:

```python
import io
import os

import discord
from discord import app_commands
from discord.ext import commands

from config import branded_embed, panel, BANNERS

STAFF_ROLE_NAME = os.getenv("STAFF_ROLE_NAME", "Staff")

CATEGORIES = [
    ("General Support", "Questions or feedback", "💬"),
    ("Payment / Refund", "Billing help", "💳"),
    ("Partnership", "Work together", "🤝"),
]


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Tickets(bot))
```

Add `"cogs.tickets"` to `COGS`.

## Step 2 — Creating the ticket channel

The heart of the system. Add this function **above** the `Tickets` class:

```python
async def create_ticket(interaction: discord.Interaction, category: str):
    guild, author = interaction.guild, interaction.user

    existing = discord.utils.get(guild.text_channels, name=f"ticket-{author.id}")
    if existing:
        await interaction.response.send_message(
            f"You already have a ticket open: {existing.mention}", ephemeral=True)
        return

    staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
    }
    if staff_role:
        overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

    channel = await guild.create_text_channel(
        name=f"ticket-{author.id}", overwrites=overwrites,
        topic=f"{category} ticket for {author}")

    embed = branded_embed(
        title=f"{category} ticket",
        description=f"Hey {author.mention}, a staff member will be with you soon.\n"
                    "Use the button below when you're done.")
    await channel.send(content=author.mention, embed=embed, view=CloseTicket())
    await interaction.response.send_message(f"Your ticket is ready: {channel.mention}", ephemeral=True)
```

The key idea is **permission overwrites** — hide the channel from `@everyone`, then add the
author and Staff back in. One ticket per person is enforced by the `existing` check.

## Step 3 — The Close button (with transcript)

Add this class above `create_ticket`:

```python
class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒",
                       custom_id="ticket:close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        await interaction.response.send_message("Saving transcript and closing…")

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
```

We walk every message with `channel.history()`, glue them into one string (remember building
up a result in a loop?), wrap it in a file, drop it in `#ticket-logs`, then delete the
channel.

## Step 4 — The dropdown + panel View

```python
class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=l, description=d, emoji=e)
                   for l, d, e in CATEGORIES]
        super().__init__(placeholder="Select what you need help with…",
                         options=options, custom_id="ticket:open")

    async def callback(self, interaction: discord.Interaction):
        await create_ticket(interaction, self.values[0])


class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())
```

## Step 5 — Persistence + the panel command

Add these methods **inside** the `Tickets` class:

```python
    async def cog_load(self):
        self.bot.add_view(TicketPanel())
        self.bot.add_view(CloseTicket())

    @app_commands.command(description="Post the ticket panel (staff only).")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def ticketpanel(self, interaction: discord.Interaction):
        embeds = panel(title="🎫 | Support",
                       description="Pick an option below to open a private ticket.",
                       banner=BANNERS.get("assistance"))
        await interaction.channel.send(embeds=embeds, view=TicketPanel())
        await interaction.response.send_message("Panel posted!", ephemeral=True)
```

`cog_load` re-registers the Views on startup so old panels never break — that's the
persistence pattern from the UI module.

## Step 6 — Test the whole flow

**▶ Run the bot** and:
1. `/ticketpanel` — the branded panel appears.
2. Pick a category from the dropdown → a private `ticket-…` channel is created.
3. Chat a little, then click **Close** → the channel deletes and a transcript lands in
   `#ticket-logs`.
4. Restart the bot and use an old panel — it still works. 🎉

## Take it further

- Add a **Claim** button so a staff member can claim a ticket.
- Store an open-ticket count per user in JSON.
- Use a **modal** (from the UI module) to ask for order details when the ticket opens.

## Recap

You built a real, production-style ticket system: dropdown → permission-overwritten private
channel → transcript → persistent Views. This single project exercises embeds, components,
permissions, files, and persistence together — the core of nearly every advanced bot.

→ **Next: Project — Economy & Leveling**
