# A Logging System

A **mod-log** keeps a record of what happens in your server — messages deleted, members
joining and leaving, edits. When something goes wrong, the log tells you what happened. It's
a great exercise because it ties together events, embeds, and channel lookups.

## Step 1 — The cog

Make `cogs/logs.py`. We'll post every log entry to a channel named `mod-logs`:

```python
import discord
from discord.ext import commands

LOG_CHANNEL = "mod-logs"


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def log_channel(self, guild):
        return discord.utils.get(guild.text_channels, name=LOG_CHANNEL)


async def setup(bot):
    await bot.add_cog(Logs(bot))
```

Add `"cogs.logs"` to `COGS` and create a `mod-logs` channel (hide it from regular members).
`log_channel()` is a little helper so we don't repeat the lookup in every event.

## Step 2 — Log deleted messages

```python
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        channel = self.log_channel(message.guild)
        if not channel:
            return

        embed = discord.Embed(
            title="🗑️ Message Deleted",
            description=message.content or "*(no text)*",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Author", value=message.author.mention)
        embed.add_field(name="Channel", value=message.channel.mention)
        await channel.send(embed=embed)
```

## Step 3 — Log edited messages

```python
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        channel = self.log_channel(before.guild)
        if not channel:
            return

        embed = discord.Embed(title="✏️ Message Edited", color=discord.Color.orange(),
                              timestamp=discord.utils.utcnow())
        embed.add_field(name="Before", value=before.content or "*(empty)*", inline=False)
        embed.add_field(name="After", value=after.content or "*(empty)*", inline=False)
        embed.add_field(name="Author", value=before.author.mention, inline=False)
        await channel.send(embed=embed)
```

Notice `on_message_edit` gives you **two** messages — `before` and `after`. We skip it if the
text didn't actually change (edits also fire when embeds load).

## Step 4 — Log joins and leaves

```python
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.log_channel(member.guild)
        if channel:
            embed = discord.Embed(description=f"📥 {member.mention} **joined**",
                                  color=discord.Color.green(), timestamp=discord.utils.utcnow())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.log_channel(member.guild)
        if channel:
            embed = discord.Embed(description=f"📤 {member.mention} **left**",
                                  color=discord.Color.dark_grey(), timestamp=discord.utils.utcnow())
            await channel.send(embed=embed)
```

> 💡 The same `on_member_join` can live in both your Welcome cog and your Logs cog —
> discord.py calls **all** listeners for an event, across every cog. One does the public
> greeting, the other does the private log.

## Step 5 — Log moderation actions (tie it together)

You can call the log from your moderation commands too. A clean way is a tiny helper other
cogs can reach:

```python
# in your /ban command, after banning:
        logs = self.bot.get_cog("Logs")
        if logs:
            channel = logs.log_channel(interaction.guild)
            if channel:
                await channel.send(f"🔨 {interaction.user.mention} banned {member} — {reason}")
```

`self.bot.get_cog("Logs")` grabs another cog so cogs can cooperate.

## Practice

**Challenge:** add a log for when a member's nickname changes. (Hint: `on_member_update`
gives you `before` and `after`; compare `before.nick != after.nick`.)

<details><summary>Solution</summary>

```python
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick == after.nick:
            return
        channel = self.log_channel(before.guild)
        if channel:
            await channel.send(
                f"✏️ {after.mention} changed nickname: `{before.nick}` → `{after.nick}`")
```
</details>

## Recap

- A logging cog listens to events (`on_message_delete/edit`, `on_member_join/remove`) and
  posts embeds to a `mod-logs` channel.
- `on_message_edit`/`on_member_update` give **before** and **after** — compare them.
- Multiple cogs can handle the same event; `bot.get_cog("Name")` lets cogs cooperate.

→ **Next: Saving Data with JSON**
