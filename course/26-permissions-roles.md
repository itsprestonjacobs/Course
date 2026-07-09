# Permissions & Role Hierarchy

Before we write moderation commands, we need to understand two things Discord cares about a
lot: who's *allowed* to run a command, and whether the bot is *ranked high enough* to act.
Getting these clear now prevents the most frustrating bugs in the whole course.

## Locking a command to staff

You don't want just anyone running `/ban`. discord.py can gate a command behind a Discord
permission with one decorator:

```python
from discord import app_commands

    @app_commands.command(description="A staff-only command.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def staff_only(self, interaction: discord.Interaction):
        await interaction.response.send_message("You're staff! ✅")
```

`@app_commands.checks.has_permissions(ban_members=True)` means: only members who have the
**Ban Members** permission can use this command. Everyone else is refused automatically —
you write no extra code for that.

Common permission checks:

```python
@app_commands.checks.has_permissions(kick_members=True)
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.checks.has_permissions(moderate_members=True)   # timeouts
@app_commands.checks.has_permissions(manage_roles=True)
@app_commands.checks.has_permissions(manage_guild=True)       # server-wide admin tasks
```

## Handling the refusal nicely

When someone without permission tries the command, discord.py raises a
`MissingPermissions` error. Catch it per-cog so the message is friendly:

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

Put this method in any moderation cog and every command in it gets the clean refusal for
free.

## Role hierarchy — the #1 gotcha

Discord has a strict rule: **you can only act on members ranked *below* you.** This applies
to the bot too. The bot can only kick/ban/timeout members whose highest role is **below the
bot's own highest role**.

Two consequences:

1. **Drag the bot's role near the top** of Server Settings → Roles. If the bot's role is at
   the bottom, it can't moderate anyone.
2. **Check hierarchy in your code** so a mod can't act on someone equal or above them:

```python
if member.top_role >= interaction.user.top_role:
    await interaction.response.send_message(
        "You can't act on someone ranked equal to or above you.", ephemeral=True)
    return
```

`member.top_role` is a member's highest role; roles compare with `>` and `<` by position.

## The two failure modes, side by side

| Symptom | Cause | Fix |
|---------|-------|-----|
| "You don't have permission" | *the user* lacks the permission | intended — they're not staff |
| "Missing Permissions" *when the command runs* | *the bot* is ranked too low or lacks the permission | drag bot role up / re-invite with the permission |

Keep this table handy — it explains almost every moderation problem.

## Recap

- Gate commands with `@app_commands.checks.has_permissions(...)`.
- Catch `MissingPermissions` in `cog_app_command_error` for a friendly refusal.
- **Role hierarchy:** the bot (and each mod) can only act on members ranked below them —
  drag the bot's role up and check `top_role` in code.

→ **Next: Kick, Ban & Unban**
