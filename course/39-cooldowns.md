# Cooldowns & Rate Limits

Without limits, people spam your commands — farming XP, opening tickets endlessly, hammering
a web API. **Cooldowns** stop that by making a user wait between uses. This short lesson also
explains Discord's own **rate limits**.

## Adding a cooldown to a command

discord.py has a decorator for this:

```python
from discord import app_commands

    @app_commands.command(description="Claim a reward.")
    @app_commands.checks.cooldown(1, 60)      # 1 use per 60 seconds, per user
    async def reward(self, interaction: discord.Interaction):
        await interaction.response.send_message("🎁 Here's your reward!")
```

`cooldown(1, 60)` means "1 use every 60 seconds." If someone tries again too soon,
discord.py raises a `CommandOnCooldown` error.

## Handling the cooldown message

Catch it in your cog's error handler so the user sees a friendly countdown:

```python
    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"⏳ Slow down! Try again in {error.retry_after:.0f} seconds.", ephemeral=True)
        else:
            raise error
```

`error.retry_after` is how many seconds are left.

## Different cooldown scopes

By default the cooldown is per user. You can change what it applies to:

```python
from discord.app_commands import checks

@checks.cooldown(1, 30)                     # per user (default)
@checks.cooldown(1, 30, key=lambda i: i.guild_id)   # per server
@checks.cooldown(1, 5, key=None)            # global, everyone shares it
```

Use per-server for things like a raffle, global for expensive shared work.

## A cooldown for your economy

Remember the leveling system? Right now someone could farm XP by spamming. A simple fix is
to track the last time each user earned XP and skip if it's too soon — a manual cooldown in
a dictionary:

```python
import time

    def __init__(self, bot):
        self.bot = bot
        self.last_xp = {}      # user_id -> timestamp

    # inside on_message:
        now = time.time()
        if now - self.last_xp.get(message.author.id, 0) < 60:
            return             # earned XP in the last 60s — skip
        self.last_xp[message.author.id] = now
        db.add(message.author.id, coins=1, xp=5)
```

Now chatting rewards XP at most once a minute — no spam farming.

## Discord's rate limits (the other kind)

Discord itself limits how fast bots can send requests — roughly a handful of messages per
channel per few seconds. If you blast messages in a tight loop, you'll get **rate limited**
and your bot pauses. discord.py handles this automatically (it waits and retries), but the
lesson is: **don't send messages in a fast loop.** If you must send many, add a small
`await asyncio.sleep(1)` between them.

## Practice

**Challenge:** add a `@checks.cooldown(1, 300)` (once per 5 minutes) to a `/report` command
and make sure the error handler shows the remaining time.

## Recap

- `@app_commands.checks.cooldown(uses, seconds)` limits how often a command runs.
- Catch `CommandOnCooldown` and show `error.retry_after`.
- Change scope with a `key` (per user / per server / global).
- Discord **rate limits** bots — don't send in fast loops; sleep between bulk sends.

→ **Next: Error Handling & a Help Command**
