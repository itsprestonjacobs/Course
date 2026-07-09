# Organizing with Cogs

So far everything lives in `main.py`. As we add embeds, moderation, tickets, and an economy,
that file would become thousands of lines. Real bots split features into **cogs** — one file
per feature. This lesson sets up that structure for the rest of the course.

## What a cog is

A cog is a class that groups related commands and events, in its own file. Your `main.py`
just **loads** the cogs. Think of cogs as chapters and `main.py` as the table of contents.

## Step 1 — The cog template

Make a folder called `cogs`. Inside it, make `general.py`:

```python
import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Check if the bot is alive.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong! 🏓")


async def setup(bot):
    await bot.add_cog(General(bot))
```

Three differences from before:
- Commands live **inside a class** and use `@app_commands.command` (not `@bot.tree.command`).
- Every command's first parameter is now `self` (because it's a method — remember classes?).
- The file **must** end with an `async def setup(bot)` function. That's what lets `main.py`
  load it.

## Step 2 — Load cogs from main.py

Update `main.py` to load your cogs on startup:

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

COGS = ["cogs.general"]      # add more cogs to this list as you build them


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

Notice `bot.run(TOKEN)` became `async def main()` with `bot.start(TOKEN)` — that's the async
way to start the bot *and* load extensions cleanly.

**▶ Run it.** `/ping` should still work, but now it lives in a tidy cog.

## Events inside cogs

Events work in cogs too — just use `@commands.Cog.listener()` instead of `@bot.event`:

```python
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} joined!")
```

## The workflow for every new feature

From here on, each feature follows the same three steps:

1. Make a new file in `cogs/` (e.g. `moderation.py`) with the class + `setup`.
2. Add `"cogs.moderation"` to the `COGS` list in `main.py`.
3. Restart the bot.

That's the rhythm for the rest of the course.

## Practice

Move your `/hello` command into a new `cogs/fun.py`, add it to `COGS`, and confirm it works.

<details><summary>Solution</summary>

```python
# cogs/fun.py
import discord
from discord import app_commands
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Say hello.")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")


async def setup(bot):
    await bot.add_cog(Fun(bot))
```

Then add `"cogs.fun"` to `COGS`.
</details>

## Recap

- A **cog** is a feature in its own file: a `commands.Cog` class + an `async def setup(bot)`.
- Commands use `@app_commands.command` and take `self` first.
- `main.py` loads cogs from a `COGS` list.
- New feature = new file + add to `COGS` + restart.

→ **Next: Sending Messages & DMs**
