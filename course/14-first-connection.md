# First Connection

Time to bring the bot online. We'll keep the token safe, write the smallest possible bot,
and see that green dot appear.

## Step 1 — Keep the token out of your code

Never paste your token directly into a `.py` file. Instead, make a file named exactly
`.env` in your project folder and put your token in it:

```
DISCORD_TOKEN=paste-your-real-token-here
GUILD_ID=
```

`GUILD_ID` is optional but very useful. Turn on **Developer Mode** in Discord (User
Settings → Advanced), then right-click your server icon → **Copy Server ID** and paste it
after the `=`. This makes new slash commands appear **instantly** instead of taking up to an
hour to register globally.

> 🔒 Make a second file named `.gitignore` with one line: `.env`. That stops your token from
> ever being uploaded if you use Git later.

## Step 2 — Write the bot

Create `main.py` and type this in:

```python
import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot.run(TOKEN)
```

## What each part does

- `load_dotenv()` + `os.getenv(...)` read your token from the `.env` file.
- `intents` matches the switches you flipped in the portal.
- `bot = commands.Bot(...)` creates the bot object.
- `@bot.event` + `on_ready` runs once, right after the bot logs in.
- `bot.run(TOKEN)` logs in and starts everything.

## Step 3 — Run it

In the terminal (with `(venv)` showing):

```
python main.py
```

You should see **`Logged in as YourBot#1234`** in the terminal, and the bot's dot turns
green in Discord. 🎉 It's alive.

To stop the bot, click the terminal and press **Ctrl + C**.

> ⚠️ **Crash with `PrivilegedIntentsRequired`?** You didn't switch on the intents in the
> developer portal (Lesson: Intents & Permissions). **`LoginFailure`?** The token in `.env`
> is wrong — reset it and paste the new one.

## Step 4 — Prove it's listening

Add this event above `bot.run(TOKEN)` to make the bot react to messages:

```python
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return                      # ignore the bot's own messages
    if message.content == "hello":
        await message.channel.send("Hi there! 👋")
```

Restart the bot, type `hello` in your server, and it replies. You just wrote your first
event handler. Next lesson we explore what other events you can hook into.

## Recap

- Token lives in `.env`, read with `python-dotenv` — never hardcoded.
- A minimal bot: intents → `commands.Bot` → `on_ready` → `bot.run(TOKEN)`.
- `on_message` is your first **event** — the bot reacts to messages.

→ **Next: Events**
