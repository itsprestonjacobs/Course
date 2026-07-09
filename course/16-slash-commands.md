# Slash Commands

Slash commands are the modern way to control a bot: you type `/` in Discord and pick from a
menu. Discord shows the command list, describes each one, and provides input boxes. Let's
add your first.

## Step 1 — Sync on startup

Discord needs to be *told* which slash commands exist. That's called **syncing**. Update
your `on_ready` to sync when the bot starts:

```python
import os

GUILD_ID = os.getenv("GUILD_ID")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if GUILD_ID:
        guild = discord.Object(id=int(GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
    else:
        synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
```

- `bot.tree` is the list of slash commands ("the command tree").
- Syncing to a specific `guild` (your test server, via `GUILD_ID`) makes commands appear
  **instantly**. Global syncing can take up to an hour.

## Step 2 — Your first slash command

Add this above `bot.run(TOKEN)`:

```python
@bot.tree.command(description="Check if the bot is alive.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")
```

- `@bot.tree.command(...)` registers a slash command. The function name `ping` becomes
  `/ping`.
- Every slash command receives an **`interaction`** — the object representing "someone just
  used this command."
- `interaction.response.send_message(...)` is how a slash command replies. (Note: it's
  `interaction.response.send_message`, not `channel.send`.)

## Step 3 — Run it

```
python main.py
```

Wait for `Synced N commands`, then in Discord type `/` and pick **ping**. The bot replies
**Pong! 🏓**. That's the full round trip.

## Public vs. private replies

By default everyone sees the reply. Add `ephemeral=True` to make it visible only to the
person who ran the command — great for "here's your info" or error messages:

```python
await interaction.response.send_message("Only you can see this.", ephemeral=True)
```

## The 3-second rule

A slash command must respond within **3 seconds** or Discord marks it "failed." For slow
work (deleting many messages, calling a web API), buy more time with `defer()`:

```python
await interaction.response.defer()          # "working on it…"
# ... slow work ...
await interaction.followup.send("Done!")    # reply after deferring
```

## Practice

Add a `/hello` command that greets the user by name:

```python
@bot.tree.command(description="Say hello.")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")
```

`interaction.user` is whoever ran the command. **Challenge:** add a `/servername` command
that replies with `interaction.guild.name`.

<details><summary>Solution</summary>

```python
@bot.tree.command(description="Show the server name.")
async def servername(interaction: discord.Interaction):
    await interaction.response.send_message(f"This server is **{interaction.guild.name}**.")
```
</details>

## Recap

- **Sync** commands in `on_ready`; sync to your test `guild` for instant updates.
- `@bot.tree.command()` makes a slash command; it receives an `interaction`.
- Reply with `interaction.response.send_message(...)`; add `ephemeral=True` for private.
- Respond within 3 seconds, or `defer()` then `followup.send(...)`.

→ **Next: Command Arguments**
