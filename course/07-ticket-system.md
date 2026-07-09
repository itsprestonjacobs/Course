# Lesson 07 — Ticket System

This is the big one. We're building the support-ticket panel you see on Derpy's Designs: a
branded panel with a **dropdown menu**. When someone picks an option, the bot spins up a
private channel only they and staff can see, with a **Close** button that saves a
transcript and deletes the channel.

It sounds like a lot, but we'll build it in small pieces and run as we go. New concept
here: **Views** — the buttons and dropdowns you attach to a message.

---

## Step 0 — Server prep

In your test server, create:
- a **role** called `Staff` (this role will see tickets),
- optionally a **channel** called `ticket-logs` (closed-ticket transcripts land here).

---

## Step 1 — New cog, wired up

Make `cogs/tickets.py`:

```python
import io
import os

import discord
from discord import app_commands
from discord.ext import commands

from config import BRAND_COLOR, STUDIO_NAME, BANNERS, branded_embed, panel

STAFF_ROLE_NAME = os.getenv("STAFF_ROLE_NAME", "Staff")


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Tickets(bot))
```

Add it to `main.py`:

```python
COGS = ["cogs.embeds", "cogs.moderation", "cogs.tickets"]
```

**▶ Run it** — should start with no errors.

---

## Step 2 — The Close button (a View)

A **View** is a box that holds buttons/dropdowns. Let's make the simplest one: a single
red **Close** button. Add this class **above** the `Tickets` class:

```python
class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red,
                       emoji="🔒", custom_id="ticket:close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Closing…")
        await interaction.channel.delete()
```

- `timeout=None` keeps the button working forever (even after the bot restarts).
- `@discord.ui.button(...)` turns the method below it into a clickable button.
- `custom_id` is a permanent name for the button — we need it for the "works after restart"
  trick later.

We'll test this in a moment once tickets exist.

---

## Step 3 — Creating the ticket channel

This is the heart of the system: make a private channel for the person who opened the
ticket. Add this function **above** the `CloseTicket` class:

```python
async def create_ticket(interaction: discord.Interaction, category: str):
    guild = interaction.guild
    author = interaction.user

    # Don't let someone open a second ticket if they already have one.
    existing = discord.utils.get(guild.text_channels, name=f"ticket-{author.id}")
    if existing:
        await interaction.response.send_message(
            f"You already have a ticket open: {existing.mention}", ephemeral=True)
        return

    staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)

    # Hide from everyone; allow the author, staff, and the bot.
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
        topic=f"{category} ticket for {author}",
    )

    embed = branded_embed(
        title=f"{category} ticket",
        description=f"Hey {author.mention}, a staff member will be with you soon.\n"
                    "Use the button below when you're done.",
    )
    await channel.send(content=author.mention, embed=embed, view=CloseTicket())
    await interaction.response.send_message(f"Your ticket is ready: {channel.mention}", ephemeral=True)
```

The key idea is **permission overwrites** — a per-channel list of who can see it. We hide
it from `@everyone`, then add the author and the Staff role back in. Notice the Close
button gets attached with `view=CloseTicket()`.

---

## Step 4 — The dropdown

Now the menu people pick from. First, list your categories near the top of the file (under
`STAFF_ROLE_NAME`):

```python
CATEGORIES = [
    ("General Support", "Questions, feedback, or anything else", "💬"),
    ("Payment / Refund", "Billing and refund help", "💳"),
    ("Partnership", "Partnership and event requests", "🤝"),
]
```

Then add the dropdown class (put it above the `Tickets` class):

```python
class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=label, description=desc, emoji=emoji)
            for label, desc, emoji in CATEGORIES
        ]
        super().__init__(placeholder="Select what you need help with…",
                         options=options, custom_id="ticket:open")

    async def callback(self, interaction: discord.Interaction):
        await create_ticket(interaction, self.values[0])


class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())
```

- A `Select` is a dropdown. Each `SelectOption` is a row in it.
- `callback` runs when someone picks an option. `self.values[0]` is what they chose, and we
  hand it straight to `create_ticket`.
- `TicketPanel` is the View that holds the dropdown.

Want to change the options later? Just edit the `CATEGORIES` list — that's the whole point
of keeping it up top.

---

## Step 5 — The /ticketpanel command

Add this command **inside** the `Tickets` class so staff can post the panel:

```python
    @app_commands.command(description="Post the ticket panel here (staff only).")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def ticketpanel(self, interaction: discord.Interaction):
        embeds = panel(
            title="🎫 | Support",
            description="Need a hand? Pick an option from the dropdown below to open a "
                        "private ticket.",
            banner=BANNERS.get("assistance"),
        )
        await interaction.channel.send(embeds=embeds, view=TicketPanel())
        await interaction.response.send_message("Panel posted!", ephemeral=True)
```

Add an `"assistance"` key to your `BANNERS` dict back in `config.py` (set it to a banner
image link, or `None` for now):

```python
BANNERS = {"welcome": None, "assistance": None}
```

**▶ Run it.** Use `/ticketpanel`, then pick an option in the dropdown. A private
`ticket-…` channel appears with a welcome embed and a Close button. Click **Close** — the
channel deletes. It works!

---

## Step 6 — Make the buttons survive a restart

There's one catch: right now, if you restart the bot, the old panel's dropdown and close
buttons stop responding. Fix it by re-registering the Views on startup. Add this method
inside the `Tickets` class:

```python
    async def cog_load(self):
        self.bot.add_view(TicketPanel())
        self.bot.add_view(CloseTicket())
```

Because we gave every button and dropdown a `custom_id`, Discord can reconnect them to the
code after a restart. **▶ Restart the bot and click an old panel** — it works now.

---

## Step 7 — Save a transcript on close

Deleting a ticket loses the conversation. Let's save it first. Replace your `close` method
in `CloseTicket` with this fuller version:

```python
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red,
                       emoji="🔒", custom_id="ticket:close")
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

- `channel.history(...)` walks through every message in the ticket.
- We build one big text string, wrap it in a file, and drop it in `#ticket-logs` before
  deleting the channel.

**▶ Final test:** open a ticket, chat a little, hit Close. The channel disappears and a
`.txt` transcript shows up in `#ticket-logs`.

---

## You built a ticket system! 🎉

Dropdown menu, private channels, permissions, persistent buttons, and transcripts — that's
a feature plenty of paid bots charge for. Compare your `cogs/tickets.py` against the one in
the `bot/` folder if anything misbehaves. Last stop: keeping your bot online 24/7.

→ **Lesson 08: Hosting & next steps**
