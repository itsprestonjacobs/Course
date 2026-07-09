# Auto-moderation

Manual moderation can't catch everything. **Auto-moderation** is your bot watching every
message and acting instantly — deleting banned words, blocking invite links, and slowing
spammers. It's all built on the `on_message` event.

## Step 1 — The cog

Make `cogs/automod.py`:

```python
import discord
from discord.ext import commands

BANNED_WORDS = ["badword1", "badword2", "scam"]


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(AutoMod(bot))
```

Add `"cogs.automod"` to `COGS`. (For this to work, the **Message Content Intent** must be
on — see the Intents lesson.)

## Step 2 — A word filter

```python
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return                                   # ignore bots and DMs

        # Don't moderate staff
        if message.author.guild_permissions.manage_messages:
            return

        content = message.content.lower()
        if any(word in content for word in BANNED_WORDS):
            await message.delete()
            warning = await message.channel.send(
                f"{message.author.mention}, watch your language! ⚠️")
            await warning.delete(delay=5)            # auto-remove the warning after 5s
```

Line by line:
- Skip bots, DMs, and staff (people who can already manage messages).
- `any(word in content for word in BANNED_WORDS)` — is *any* banned word in the message?
  (You saw `any(...)` back in the logic lesson.)
- Delete the message, post a warning, and clean the warning up after 5 seconds.

**▶ Test** by adding a harmless test word to `BANNED_WORDS` and typing it.

## Step 3 — Block invite links

Stop people advertising other servers:

```python
        if "discord.gg/" in content or "discord.com/invite" in content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, no invite links!", delete_after=5)
            return
```

`delete_after=5` is a shortcut — the message deletes itself after 5 seconds.

## Step 4 — A simple anti-spam

Catch someone sending the same message many times fast. We remember each user's last message
in a dictionary (remember dictionaries?):

```python
    def __init__(self, bot):
        self.bot = bot
        self.last_message = {}     # user_id -> their last message text

    # inside on_message, after the staff check:
        if self.last_message.get(message.author.id) == content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, stop spamming!", delete_after=5)
        self.last_message[message.author.id] = content
```

This is deliberately simple. Discord also has a built-in **AutoMod** feature (Server
Settings → AutoMod) for heavy-duty filtering — but building your own teaches you how it
works and gives you full control.

## Practice

**Challenge:** add an ALL-CAPS filter that deletes messages longer than 10 characters that
are entirely uppercase. (Hint: `message.content.isupper()` and `len(message.content) > 10`.)

<details><summary>Solution</summary>

```python
        if len(message.content) > 10 and message.content.isupper():
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, no need to shout!", delete_after=5)
```
</details>

## Recap

- Auto-mod lives in an `on_message` listener (needs the **Message Content Intent**).
- Always skip bots, DMs, and staff first.
- Techniques: word filter with `any(...)`, invite-link block, and a dictionary-based
  anti-spam.
- `delete_after=` / `delete(delay=)` auto-clean warning messages.

→ **Next: A Logging System**
