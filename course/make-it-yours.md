# Make It Yours: One-File Setup

Your bot shouldn't be hardcoded to one server. This lesson gathers **every setting into a
single file — `config.py`** — so anyone can rebrand and reconfigure the bot without touching
the cogs. Change it here; the whole bot updates.

## The control panel

Here's the full `config.py`. Everything above the helpers is meant to be edited:

```python
import os
import discord

# ---- Branding ----
STUDIO_NAME = "Derpy's Designs"
TAGLINE = "Where Creativity Meets Precision"
BRAND_COLOR = discord.Color.from_str("#1e9bff")

BANNERS = {"welcome": None, "assistance": None, "market": None}   # paste image links
DIVIDER_IMAGE = None

# ---- Roles (match the names in YOUR server) ----
STAFF_ROLE_NAME = os.getenv("STAFF_ROLE_NAME", "Staff")
AUTO_ROLE_NAME = "Member"        # given to new members (None to disable)

# ---- Channels (create these in your server) ----
WELCOME_CHANNEL = "welcome"
LOG_CHANNEL = "mod-logs"
TICKET_LOG_CHANNEL = "ticket-logs"

# ---- Self-role menu: (label, emoji, role name) ----
ROLE_BUTTONS = [
    ("Announcements", "📢", "Announcements"),
    ("Events", "🎉", "Events"),
    ("Updates", "🔔", "Updates"),
]

# ---- Ticket categories: (label, description, emoji) ----
TICKET_CATEGORIES = [
    ("Place an Order", "Order a custom design or bot", "🛒"),
    ("General Support", "Questions, feedback, or help", "💬"),
    ("Payment / Refund", "Billing, invoices, and refunds", "💳"),
    ("Claim a Purchase", "Claim a purchased role or ad", "🎟️"),
    ("Partnership", "Partnerships and collaborations", "🤝"),
    ("Staff Report", "Report a problem or staff concern", "🛡️"),
]

# ---- Auto-moderation ----
BANNED_WORDS = ["scam", "free nitro"]
BLOCK_INVITE_LINKS = True

# ---- Economy ----
COINS_PER_MESSAGE = 1
XP_PER_MESSAGE = 5
DAILY_REWARD = 100
```

Every cog imports from here. For example, the ticket cog does
`from config import TICKET_CATEGORIES`, so editing that one list changes the whole ticket
panel.

## Common changes

**Rebrand it:** change `STUDIO_NAME`, `TAGLINE`, and `BRAND_COLOR`. Done — every embed
updates.

**Change what people can open tickets for:** edit `TICKET_CATEGORIES`. Add a row, remove
one, change an emoji:

```python
TICKET_CATEGORIES = [
    ("Buy a Bot", "Order a custom Discord bot", "🤖"),
    ("Report a Bug", "Something's broken", "🐛"),
]
```

**Change the self-roles menu:** edit `ROLE_BUTTONS` with your own role names (they must
exist in your server).

**Change auto-mod words or rewards:** edit `BANNED_WORDS`, or the `COINS_PER_MESSAGE` /
`DAILY_REWARD` numbers.

## Using names vs. role IDs

The config uses role and channel **names** because they're easy to read. Names work great
as long as they match your server exactly (they're case-sensitive).

If you'd rather use **IDs** (which never break even if you rename a role), turn on Developer
Mode in Discord, right-click a role → **Copy Role ID**, and look it up by ID instead:

```python
STAFF_ROLE_ID = 123456789012345678       # in config.py

# in a cog:
staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
```

IDs are more robust; names are more beginner-friendly. Pick whichever you prefer — the bot
works with both.

## Runtime setup commands

For settings that differ per server, you don't even need to edit the file — the bot has
commands (from the settings lesson):

- `/set_welcome #channel` — where welcome messages go.
- `/set_logs #channel` — where logs go.

These save to `settings.json` and override the config defaults for that server.

## Practice

**Challenge:** rebrand the bot to your own studio — change `STUDIO_NAME`, `BRAND_COLOR`, and
one ticket category — then restart and confirm `/serverinfo` and `/ticketpanel` show your
new branding.

## Recap

- **`config.py` is the control panel** — names, colors, channels, roles, ticket categories,
  banned words, and rewards, all in one place.
- Cogs import from it, so one edit updates the whole bot.
- Use **names** (easy) or **IDs** (robust) for roles/channels; per-server settings live in
  `/set_*` commands.

→ **Next: Host It 24/7**
