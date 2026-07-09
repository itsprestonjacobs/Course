# Per-Server Settings

If your bot is ever in more than one server, hardcoding channel names like `"welcome"` or
`"mod-logs"` breaks down — every server is different. This lesson makes your bot
**configurable**: each server's admins choose their own channels, and the bot remembers.

## The idea

Store a small settings dictionary **per server**, keyed by the server's ID. We'll use JSON
(from the JSON lesson) since settings are small.

```json
{
  "111222333": { "welcome_channel": "welcome", "log_channel": "mod-logs" },
  "444555666": { "welcome_channel": "lobby",   "log_channel": "audit" }
}
```

Each top-level key is a **guild ID**; each value is that server's settings.

## Step 1 — A settings helper

Reusing the `data.py` from the JSON lesson, make `settings.py`:

```python
import data

FILE = "settings.json"
_settings = data.load(FILE, {})


def get(guild_id, key, default=None):
    return _settings.get(str(guild_id), {}).get(key, default)


def set_value(guild_id, key, value):
    gid = str(guild_id)
    _settings.setdefault(gid, {})
    _settings[gid][key] = value
    data.save(FILE, _settings)
```

- `get(guild_id, key, default)` reads a setting, with a fallback.
- `set_value(...)` updates it and saves.

## Step 2 — A command to configure it

Make `cogs/settings.py`:

```python
import discord
from discord import app_commands
from discord.ext import commands

import settings


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Set the welcome channel.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_welcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        settings.set_value(interaction.guild.id, "welcome_channel", channel.name)
        await interaction.response.send_message(
            f"Welcome messages will now go to {channel.mention}.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Settings(bot))
```

Now an admin runs `/set_welcome channel:#lobby` and the bot remembers it — even after a
restart, even across different servers.

## Step 3 — Read the setting where you need it

Update the Welcome cog to *use* the stored channel instead of a hardcoded name:

```python
import settings

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_name = settings.get(member.guild.id, "welcome_channel", "welcome")
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            await channel.send(f"Welcome, {member.mention}!")
```

Notice the default `"welcome"` — if an admin never set one, it falls back gracefully.

## Why this matters

This is the difference between a personal bot and one you could share with other servers (or
even publish). Every feature that references a specific channel or role — welcome, logs,
tickets, automod — can read from `settings` instead of a hardcoded value. Same code, works
everywhere.

## Practice

**Challenge:** add a `/set_logs` command that stores the `log_channel` setting, then update
your Logs cog's `log_channel()` helper to read
`settings.get(guild.id, "log_channel", "mod-logs")`.

<details><summary>Solution</summary>

```python
    @app_commands.command(description="Set the mod-log channel.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_logs(self, interaction, channel: discord.TextChannel):
        settings.set_value(interaction.guild.id, "log_channel", channel.name)
        await interaction.response.send_message(f"Logs will go to {channel.mention}.", ephemeral=True)

# in Logs cog:
    def log_channel(self, guild):
        name = settings.get(guild.id, "log_channel", "mod-logs")
        return discord.utils.get(guild.text_channels, name=name)
```
</details>

## Recap

- Store settings **per guild ID** so the bot works in any server.
- A `settings.py` helper wraps `get`/`set_value` over the JSON data layer.
- Read settings where you'd otherwise hardcode a channel/role name, always with a fallback.

→ **Next: Project — Ticket System**
