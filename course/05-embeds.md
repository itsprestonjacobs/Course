# Lesson 05 — Embeds

Embeds are the clean, colored boxes you see all over Derpy's Designs — a banner on top, a
bold title, description, fields, and that divider bar at the bottom. We'll build them up
one piece at a time. By the end you'll have a reusable "brand style" that makes every
future command look professional automatically.

Work through the steps **in order** and run the bot after each one so you can see what each
line adds.

---

## Step 1 — Switch main.py over to cogs

As we add features, cramming everything into `main.py` gets messy. Real bots split features
into files called **cogs**. Let's set that up now.

Make a new folder called `cogs` in your project. Then replace your `main.py` with this
version, which loads cogs and syncs commands:

```python
import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

COGS = ["cogs.embeds"]   # we'll add more cogs to this list later


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if GUILD_ID:
        guild = discord.Object(id=int(GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
    else:
        synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")


async def main():
    async with bot:
        for cog in COGS:
            await bot.load_extension(cog)
        await bot.start(TOKEN)


asyncio.run(main())
```

Don't run it yet — `cogs.embeds` doesn't exist. That's Step 3.

---

## Step 2 — Make a branding file

Here's the trick to a consistent-looking bot: keep all your branding in ONE file, then
reuse it everywhere. Make a file called `config.py` next to `main.py`:

```python
import discord

STUDIO_NAME = "Derpy's Designs"
TAGLINE = "Where Creativity Meets Precision"
BRAND_COLOR = discord.Color.from_str("#1e9bff")


def branded_embed(title=None, description=None):
    embed = discord.Embed(title=title, description=description, color=BRAND_COLOR)
    embed.set_footer(text=f"{STUDIO_NAME} • {TAGLINE}")
    return embed
```

`branded_embed()` is a small helper that hands back an embed that already has your color
and footer. Change the name or color here and **every** embed in the bot updates. (This is
your studio name — swap in whatever you like.)

---

## Step 3 — Your first embed command

Make a file `cogs/embeds.py`. We'll start with the cog skeleton and one command:

```python
import discord
from discord import app_commands
from discord.ext import commands

from config import branded_embed, STUDIO_NAME


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Show info about this server.")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild
        embed = branded_embed(title=g.name, description=f"A {STUDIO_NAME} community.")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Embeds(bot))
```

**▶ Run it now** (`python main.py`) and try `/serverinfo`. You get a small branded embed
with your server's name. It's plain — we'll fill it in next.

> The `setup` function at the bottom is what lets `main.py` load this file. Every cog needs
> one.

---

## Step 4 — Add fields

Fields are little label/value pairs. Add these lines inside `serverinfo`, right after the
`embed = ...` line:

```python
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)

        embed.add_field(name="Members", value=g.member_count, inline=True)
        embed.add_field(name="Channels", value=len(g.channels), inline=True)
        embed.add_field(name="Roles", value=len(g.roles), inline=True)
```

**▶ Run it again.** Now `/serverinfo` shows the server icon in the corner and three stats
side by side. `inline=True` is what puts them in a row instead of stacked.

Play with it: add another field for the owner —
`embed.add_field(name="Owner", value=g.owner.mention, inline=True)`.

---

## Step 5 — Panels: banner on top + divider bar

The big Derpy's Designs panels (Assistance, Market, Order Here) have an image banner on
top and a bar at the bottom. A single embed can only hold one image, so the trick is to
send **two embeds together** — Discord stacks them into one card.

Add this to the bottom of `config.py`:

```python
BANNERS = {"welcome": None}   # paste an image link here later
DIVIDER_IMAGE = None          # the thin bar at the bottom


def panel(title, description, banner=None):
    embeds = []
    if banner:
        top = discord.Embed(color=BRAND_COLOR)
        top.set_image(url=banner)
        embeds.append(top)

    body = discord.Embed(title=title, description=description, color=BRAND_COLOR)
    if DIVIDER_IMAGE:
        body.set_image(url=DIVIDER_IMAGE)
    body.set_footer(text=f"{STUDIO_NAME} • {TAGLINE}")
    embeds.append(body)
    return embeds
```

> **How do I get an image link?** Upload your banner image to any Discord channel, then
> right-click it → **Copy Link**, and paste that link as the `"welcome"` value (and as
> `DIVIDER_IMAGE` for the bar). Leaving them `None` just skips the images for now.

---

## Step 6 — A command that posts a panel

Add a second command to your `Embeds` cog. Update the import line at the top first:

```python
from config import branded_embed, panel, STUDIO_NAME, BANNERS
```

Then add this command inside the class:

```python
    @app_commands.command(description="Post a branded announcement panel.")
    @app_commands.describe(title="Panel title", message="What it should say")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def announce(self, interaction: discord.Interaction, title: str, message: str):
        await interaction.channel.send(embeds=panel(title, message, banner=BANNERS["welcome"]))
        await interaction.response.send_message("Posted!", ephemeral=True)
```

**▶ Run it** and try `/announce title:Welcome message:Thanks for joining!`. You get a
branded panel. Once you paste a real banner link into `config.py`, the same command
produces the full Derpy's Designs look — banner, title, text, divider bar.

- The extra `title` and `message` arguments become fill-in boxes in Discord.
- `@app_commands.checks.has_permissions(manage_guild=True)` means only staff can post
  panels. (More on permission checks in the next lesson.)
- `ephemeral=True` makes the "Posted!" reply visible only to you.

---

## What you've got

A branding file every future feature will reuse, a real info embed, and the panel style
that matches the studio's look. Next we lock down some commands and build the moderation
toolkit.

→ **Lesson 06: Moderation commands**
