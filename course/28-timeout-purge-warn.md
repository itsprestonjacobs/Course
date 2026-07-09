# Timeout, Purge & Warn

Three more moderation staples. Add each to your `Moderation` cog next to `/kick` and `/ban`.

## /timeout — Discord's built-in mute

You don't need a "Muted" role anymore — Discord has timeouts built in. A timed-out member
can't talk or react until it expires:

```python
import datetime

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

`datetime.timedelta(minutes=minutes)` means "this long from now." You can also do
`hours=` or `days=` (max 28 days). **▶ Test** `/timeout minutes:1`.

To remove a timeout early, pass `None`:

```python
    @app_commands.command(description="Remove a timeout.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout(self, interaction, member: discord.Member):
        await member.timeout(None)
        await interaction.response.send_message(f"Removed timeout from {member.mention}.")
```

## /purge — bulk delete messages

```python
    @app_commands.command(description="Delete recent messages.")
    @app_commands.describe(amount="How many (max 100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction, amount: int):
        amount = min(amount, 100)
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)
```

Two things worth understanding:
- `min(amount, 100)` caps it — Discord won't bulk-delete more than 100 at once.
- We `defer()` first because deleting many messages can take longer than the 3-second reply
  window (remember that rule?), then answer with `followup.send`.

**▶ Test** `/purge amount:5`.

## /warn — a warning with a DM

A warning has no built-in Discord action — we just tell the member and log it. Here's the
basic version (we'll make warnings *persist* in the data module):

```python
    @app_commands.command(description="Warn a member.")
    @app_commands.describe(member="Who", reason="What for")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction, member: discord.Member, reason: str):
        embed = result_embed("Member Warned", member, interaction.user, reason,
                             discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        try:
            await member.send(f"You were warned in **{interaction.guild.name}**: {reason}")
        except discord.Forbidden:
            pass    # their DMs are closed — nothing we can do
```

The `try / except discord.Forbidden` handles members who've disabled DMs, so the command
never crashes.

## Practice

**Challenge:** add a `/slowmode` command that takes `seconds: int` and sets the current
channel's slowmode. (Hint: `await interaction.channel.edit(slowmode_delay=seconds)` and it
needs `manage_channels=True`.)

<details><summary>Solution</summary>

```python
    @app_commands.command(description="Set channel slowmode.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction, seconds: int):
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"Slowmode set to {seconds}s.")
```
</details>

## Recap

- `member.timeout(timedelta)` mutes; `member.timeout(None)` un-mutes.
- `channel.purge(limit=n)` bulk-deletes (≤100); `defer()` first because it's slow.
- `/warn` DMs the member inside `try / except discord.Forbidden`.

→ **Next: Welcome & Leave Messages**
