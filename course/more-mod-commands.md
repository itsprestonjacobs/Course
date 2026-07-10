# More Mod Commands & Adding Your Own

You've built the core (`/kick`, `/ban`, `/timeout`, `/purge`, `/warn`). Here's the rest of a
complete moderation toolkit, how to **log every action**, and — most importantly — how to
**add your own** commands.

## The full command set

A well-rounded moderation cog includes:

| Command | What it does | Permission |
|---------|--------------|------------|
| `/kick` | Remove a member | Kick Members |
| `/ban` | Ban a member | Ban Members |
| `/unban` | Unban by user ID | Ban Members |
| `/timeout` | Mute for X minutes | Moderate Members |
| `/untimeout` | Remove a timeout | Moderate Members |
| `/purge` | Bulk-delete messages | Manage Messages |
| `/slowmode` | Set channel slowmode | Manage Channels |
| `/lock` / `/unlock` | Stop / allow @everyone talking | Manage Channels |
| `/nick` | Change a nickname | Manage Nicknames |
| `/role` | Give/remove a role | Manage Roles |
| `/warn` `/warnings` `/clearwarns` | Warning system (saved) | Moderate Members |

## Logging every action

Staff want a record. Add a helper at the top of the cog that posts each action to your
log channel:

```python
from config import LOG_CHANNEL

async def mod_log(guild, embed):
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL)
    if channel:
        await channel.send(embed=embed)
```

Then in each command, after acting, send the same embed to the log:

```python
        await member.ban(reason=reason)
        embed = result_embed("Member Banned", member, interaction.user, reason, discord.Color.red())
        await interaction.response.send_message(embed=embed)
        await mod_log(interaction.guild, embed)      # <-- log it
```

Now every kick, ban, and timeout leaves a permanent, searchable trail in `#mod-logs`.

## The new commands

**Lock / unlock a channel** — flip @everyone's ability to send messages:

```python
    @app_commands.command(description="Lock this channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message("🔒 Channel locked.")
```

`/unlock` is the same with `send_messages=None` (which clears the override).

**Nickname:**

```python
    @app_commands.command(description="Change a member's nickname.")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def nick(self, interaction, member: discord.Member, nickname: str = None):
        await member.edit(nick=nickname)
        await interaction.response.send_message(f"Nickname updated for {member.mention}.")
```

**Give/remove a role** (toggles it):

```python
    @app_commands.command(description="Give or remove a role from a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role(self, interaction, member: discord.Member, role: discord.Role):
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"Removed {role.name} from {member.mention}.")
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"Gave {role.name} to {member.mention}.")
```

`/unban`, `/untimeout`, and `/slowmode` follow the same shapes — see the `bot/` reference
for the full versions.

## How to add YOUR OWN mod command

Here's the template. Every moderation command is the same five pieces:

```python
    @app_commands.command(description="WHAT IT DOES")           # 1. register it
    @app_commands.describe(member="Who", reason="Why")         # 2. label the inputs
    @app_commands.checks.has_permissions(SOME_PERMISSION=True) # 3. who can use it
    async def MYCOMMAND(self, interaction, member: discord.Member, reason: str = None):
        if self.outranks(interaction, member):                 # 4. hierarchy safety check
            await interaction.response.send_message("Can't act on someone above you.", ephemeral=True)
            return

        await member.SOME_ACTION(reason=reason)                # 5. do the thing (+ log it)
        embed = result_embed("What Happened", member, interaction.user, reason, discord.Color.red())
        await interaction.response.send_message(embed=embed)
        await mod_log(interaction.guild, embed)
```

**Example — a `/kickall_bots` command** that kicks every bot a mod doesn't want:

```python
    @app_commands.command(description="Kick all bots except this one.")
    @app_commands.checks.has_permissions(administrator=True)
    async def kick_bots(self, interaction: discord.Interaction):
        count = 0
        for member in interaction.guild.members:
            if member.bot and member != interaction.guild.me:
                await member.kick(reason="Bot cleanup")
                count += 1
        await interaction.response.send_message(f"Kicked {count} bots.")
```

You now have the pattern to build **any** moderation command: pick the permission, add the
inputs, do the action, log it.

## Practice

**Challenge:** add a `/announce_lock` that locks the channel **and** posts a red embed
saying "This channel is now locked." Log it with `mod_log`.

## Recap

- A full mod toolkit adds unban, untimeout, slowmode, lock/unlock, nick, and role.
- A `mod_log()` helper posts every action to `#mod-logs` for a permanent record.
- To add your own: register → describe → permission check → hierarchy check → act → log.

→ **Next: Welcome & Leave Messages**
