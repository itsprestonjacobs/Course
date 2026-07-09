# Lesson 04 — Your First Bot

Time to bring the bot online. We'll write the smallest possible bot, get it logged in, and
add one slash command so you can see the whole loop work.

## Step 1 — Keep the token out of your code

Never paste your token directly in a `.py` file. Instead, make a file named exactly `.env`
in your project folder and put this inside (paste your real token):

```
DISCORD_TOKEN=your-token-goes-here
GUILD_ID=
```

`GUILD_ID` is optional but worth setting. Turn on **Developer Mode** in Discord
(User Settings → Advanced), then right-click your server icon → **Copy Server ID** and
paste it after the `=`. This makes new slash commands appear **instantly** instead of
taking up to an hour.

## Step 2 — Write the bot

Make a file called `main.py` and type this in:

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


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")

    if GUILD_ID:
        guild = discord.Object(id=int(GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
    else:
        synced = await bot.tree.sync()

    print(f"Synced {len(synced)} commands")


@bot.tree.command(description="Check if the bot is alive.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")


bot.run(TOKEN)
```

## What each part does

- **`load_dotenv()` / `os.getenv`** — reads your token from the `.env` file.
- **`intents`** — matches the switches you flipped in Lesson 03.
- **`bot = commands.Bot(...)`** — creates the bot object.
- **`on_ready`** — runs once the bot logs in; here we sync the slash commands.
- **`@bot.tree.command`** — registers a slash command. `ping` becomes `/ping`.
- **`interaction.response.send_message`** — how a slash command replies.
- **`bot.run(TOKEN)`** — logs in and starts everything.

## Step 3 — Run it

In the terminal (with `(venv)` showing):

```
python main.py
```

You should see `Logged in as ...` and `Synced 1 commands`. Your bot's dot turns green in
Discord. Go to your server, type `/`, and pick **ping**. It replies **Pong! 🏓**.

🎉 That's a working bot. To stop it, click the terminal and press **Ctrl + C**.

> ⚠️ **Nothing happened / red errors?** The two classic first-run problems are a wrong
> token and forgetting to turn on intents. Both are covered on the Troubleshooting page.

## Growing up: cogs

As we add embeds, moderation, and tickets, `main.py` would get huge. Real bots split
features into separate files called **cogs**. The finished reference bot in the `bot/`
folder is organized that way — `main.py` just loads `cogs/embeds.py`, `cogs/moderation.py`,
and `cogs/tickets.py`. From here on, each lesson builds one cog.

→ **Lesson 05: Embeds**
