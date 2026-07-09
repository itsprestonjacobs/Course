# Background Tasks & Scheduling

So far your bot only acts when something happens — a message, a command. But sometimes you
want it to do things **on a schedule**: post a daily message, check for expired mutes every
minute, back up data every hour. That's what **tasks** are for.

## The tasks.loop decorator

discord.py has a built-in looping helper. Make `cogs/tasks_demo.py`:

```python
import discord
from discord.ext import commands, tasks


class Scheduled(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.heartbeat.start()          # start the loop when the cog loads

    def cog_unload(self):
        self.heartbeat.cancel()         # stop it cleanly if the cog is unloaded

    @tasks.loop(minutes=5)
    async def heartbeat(self):
        print("Still alive! Running every 5 minutes.")

    @heartbeat.before_loop
    async def before(self):
        await self.bot.wait_until_ready()   # don't run until the bot is connected


async def setup(bot):
    await bot.add_cog(Scheduled(bot))
```

Key parts:
- `@tasks.loop(minutes=5)` — runs the function every 5 minutes. You can use `seconds=`,
  `minutes=`, or `hours=`.
- `.start()` in `__init__` kicks it off; `.cancel()` in `cog_unload` stops it.
- `@heartbeat.before_loop` + `wait_until_ready()` makes sure the bot is fully connected
  before the first run.

## A useful example: a scheduled announcement

```python
    @tasks.loop(hours=24)
    async def daily_message(self):
        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, name="general")
            if channel:
                await channel.send("☀️ Good morning! Don't forget to claim your `/daily`.")
```

## Running at a specific time each day

Instead of "every 24 hours from startup," you can run at a fixed clock time:

```python
import datetime

    @tasks.loop(time=datetime.time(hour=9, minute=0))   # 09:00 UTC every day
    async def morning(self):
        ...
```

## A real use: expiring temporary actions

Tasks are perfect for cleaning up. For example, check every minute whether any temporary
mutes have expired and lift them, or delete stale tickets. The pattern is always the same:
a `@tasks.loop`, started in `__init__`, that does a quick check each time.

## Don't block the loop

Inside a task, use `await` for anything slow (sending messages, database work over a
network), just like everywhere else. A task shares the same event loop as the rest of the
bot — that's why async matters.

## Practice

**Challenge:** make a task that runs every 30 minutes and updates the bot's status to show a
random tip. (Hint: `await self.bot.change_presence(activity=discord.Game("Type /help"))`.)

<details><summary>Solution</summary>

```python
import random

    @tasks.loop(minutes=30)
    async def rotate_status(self):
        tips = ["Type /help", "Open a /ticketpanel", "Claim your /daily"]
        await self.bot.change_presence(activity=discord.Game(random.choice(tips)))

    @rotate_status.before_loop
    async def before(self):
        await self.bot.wait_until_ready()
```
(Call `self.rotate_status.start()` in `__init__`.)
</details>

## Recap

- `@tasks.loop(minutes=/hours=/time=)` runs a function on a schedule.
- `.start()` in `__init__`, `.cancel()` in `cog_unload`, and `before_loop` +
  `wait_until_ready()`.
- Great for announcements, cleanup, status rotation, and expiring temporary actions.

→ **Next: Cooldowns & Rate Limits**
