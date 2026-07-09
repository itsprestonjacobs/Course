# Lesson 06 — Moderation Commands

Now the practical stuff: commands that keep a server tidy — `/kick`, `/ban`, `/timeout`,
`/purge`, and `/warn`. We'll add them one at a time so you see each one work before moving
on. Every command is locked so only staff can use it.

---

## Step 1 — New cog, wired up

Make a file `cogs/moderation.py` with this starter:

```python
import datetime

import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Moderation(bot))
```

Now tell `main.py` to load it. Find the `COGS` line and add the new cog:

```python
COGS = ["cogs.embeds", "cogs.moderation"]
```

**▶ Run it.** Nothing new appears yet (no commands), but it should start with no errors.
If it crashes, fix that before adding commands.

---

## Step 2 — A shared result helper

Every mod action will reply with the same style of embed: who, by whom, and why. Rather
than write that five times, add one helper **above** the class (below the imports):

```python
def result_embed(action, member, moderator, reason, color):
    embed = discord.Embed(title=action, color=color, timestamp=datetime.datetime.now())
    embed.add_field(name="Member", value=f"{member} ({member.id})", inline=False)
    embed.add_field(name="Moderator", value=moderator.mention, inline=False)
    embed.add_field(name="Reason", value=reason or "No reason given", inline=False)
    return embed
```

---

## Step 3 — /kick

Add this **inside** the `Moderation` class:

```python
    @app_commands.command(description="Kick a member from the server.")
    @app_commands.describe(member="Who to kick", reason="Why")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "You can't kick someone ranked equal to or above you.", ephemeral=True)
            return

        await member.kick(reason=reason)
        embed = result_embed("Member Kicked", member, interaction.user, reason, discord.Color.red())
        await interaction.response.send_message(embed=embed)
```

Read the important lines:
- `@app_commands.checks.has_permissions(kick_members=True)` — only people with the **Kick
  Members** permission can use it. Everyone else is refused automatically.
- The `if member.top_role >= ...` block stops a mod from kicking someone ranked above them.
- `await member.kick(...)` is the line that actually does it.

**▶ Run it** and test `/kick` on a throwaway alt account in your test server.

---

## Step 4 — /ban

Almost identical. Add it inside the class:

```python
    @app_commands.command(description="Ban a member from the server.")
    @app_commands.describe(member="Who to ban", reason="Why")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "You can't ban someone ranked equal to or above you.", ephemeral=True)
            return

        await member.ban(reason=reason)
        embed = result_embed("Member Banned", member, interaction.user, reason, discord.Color.red())
        await interaction.response.send_message(embed=embed)
```

Only three things changed from `/kick`: the name, `ban_members=True`, and
`await member.ban(...)`. **▶ Run and test.**

---

## Step 5 — /timeout (the built-in mute)

You don't need a "Muted" role anymore — Discord has timeouts built in:

```python
    @app_commands.command(description="Time a member out (mute) for some minutes.")
    @app_commands.describe(member="Who", minutes="How long", reason="Why")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction, member: discord.Member, minutes: int, reason: str = None):
        until = datetime.timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)
        embed = result_embed(f"Timed Out for {minutes} min", member,
                             interaction.user, reason, discord.Color.red())
        await interaction.response.send_message(embed=embed)
```

**▶ Test** `/timeout minutes:1` on your alt — it gets muted for a minute.

---

## Step 6 — /purge (bulk delete)

```python
    @app_commands.command(description="Delete a bunch of recent messages.")
    @app_commands.describe(amount="How many (max 100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction, amount: int):
        amount = min(amount, 100)
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)
```

Deleting lots of messages takes a moment, so we call `defer()` first — that tells Discord
"give me a sec" so it doesn't think the command failed. Afterwards we reply with
`followup.send`. **▶ Test** `/purge amount:5`.

---

## Step 7 — /warn (with a DM)

```python
    @app_commands.command(description="Warn a member (DMs them).")
    @app_commands.describe(member="Who", reason="What for")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction, member: discord.Member, reason: str):
        embed = result_embed("Member Warned", member, interaction.user, reason,
                             discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        try:
            await member.send(f"You were warned in **{interaction.guild.name}**: {reason}")
        except discord.Forbidden:
            pass  # their DMs are closed; nothing we can do
```

`try / except discord.Forbidden` catches the case where the member has DMs off, so the
command doesn't crash. **▶ Test** `/warn`.

---

## Step 8 — One friendly error message for the whole cog

Right now, when someone without permission tries a command, Discord shows an ugly error.
Add this method **inside the class** to catch that once for every command:

```python
    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            msg = "You don't have permission to use that command."
        else:
            msg = f"Something went wrong: {error}"
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
```

**▶ Test** by trying a command from an account **without** mod permissions — you now get a
clean "you don't have permission" message.

---

> ⚠️ **Command runs but says "Missing Permissions"?** That's Discord refusing the *bot*,
> not you. The bot's own role must sit **above** the member it's acting on. Fix it in
> Server Settings → Roles by dragging the bot's role up. This trips up almost everyone.

You now have a full moderation toolkit. Last big feature: the ticket system.

→ **Lesson 07: Ticket system**
