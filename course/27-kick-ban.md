# Kick, Ban & Unban

Now the real moderation commands. We'll build them in a `cogs/moderation.py` cog. Each one
uses the permission checks and hierarchy rule from the last lesson.

## Step 1 — The cog + a shared result embed

Every action replies with the same style of embed, so we make a helper once:

```python
import datetime

import discord
from discord import app_commands
from discord.ext import commands


def result_embed(action, member, moderator, reason, color):
    embed = discord.Embed(title=action, color=color, timestamp=datetime.datetime.now())
    embed.add_field(name="Member", value=f"{member} ({member.id})", inline=False)
    embed.add_field(name="Moderator", value=moderator.mention, inline=False)
    embed.add_field(name="Reason", value=reason or "No reason given", inline=False)
    return embed


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Moderation(bot))
```

Add `"cogs.moderation"` to the `COGS` list in `main.py`.

## Step 2 — /kick

```python
    @app_commands.command(description="Kick a member.")
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

`await member.kick(reason=reason)` is the line that does it. The `reason` shows up in the
server's audit log. **▶ Test** on a throwaway alt.

## Step 3 — /ban

Nearly identical — swap `kick` for `ban`:

```python
    @app_commands.command(description="Ban a member.")
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

## Step 4 — /unban

Unbanning is different: the person isn't in the server anymore, so we can't use a member
picker. We take their **user ID** (a number) and look them up:

```python
    @app_commands.command(description="Unban a user by ID.")
    @app_commands.describe(user_id="The banned user's ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction, user_id: str):
        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"Unbanned **{user}**.")
```

To get someone's ID: turn on Developer Mode, then right-click them in the ban list
(**Server Settings → Bans**) → Copy ID.

## Step 5 — The error handler

Add the friendly refusal from the last lesson so non-staff get a clean message:

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

> ⚠️ Getting "Missing Permissions" when *you* run it? That's the **bot** being ranked too
> low — drag its role above the target member (see the last lesson).

## Practice

**Challenge:** add a `/softban` that bans then immediately unbans a member — a trick that
kicks them *and* deletes their recent messages. (Hint: `member.ban(delete_message_days=1)`
then `guild.unban(member)`.)

<details><summary>Solution</summary>

```python
    @app_commands.command(description="Softban (ban + unban to clear messages).")
    @app_commands.checks.has_permissions(ban_members=True)
    async def softban(self, interaction, member: discord.Member, reason: str = None):
        await member.ban(reason=reason, delete_message_days=1)
        await interaction.guild.unban(member)
        await interaction.response.send_message(f"Softbanned **{member}**.")
```
</details>

## Recap

- `await member.kick()` / `await member.ban()` — gated by permission checks + hierarchy.
- **Unban** uses a user **ID** and `guild.unban(user)` since they've left.
- Share a `result_embed` helper and a `cog_app_command_error` handler across the cog.

→ **Next: Timeout, Purge & Warn**
