# Troubleshooting

Almost every beginner hits the same handful of errors. Find yours here before pulling your
hair out. The golden rule: **read the last few red lines in your terminal** — they almost
always name the file and line.

## Setup & startup

**`python` is not recognized**
Python isn't on your PATH. Reinstall Python and tick **"Add Python to PATH"** on the first
installer screen.

**Windows: "running scripts is disabled on this system"**
Run once, then activate the venv again:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**`ModuleNotFoundError: No module named 'discord'`**
The library isn't installed in the environment you're using. Make sure `(venv)` shows in the
terminal, then `pip install discord.py python-dotenv`.

**`No token found` / `LoginFailure: Improper token`**
- Is there a file named exactly `.env` (not `env.txt`) next to `main.py`?
- Does the line read `DISCORD_TOKEN=...` with your real token, no quotes or spaces?
- If unsure, reset the token in the Developer Portal and paste the new one.

**`PrivilegedIntentsRequired`**
You didn't switch the intents ON in the Developer Portal → your app → **Bot**. Enable
**Server Members** and **Message Content**, save, and restart.

## Commands

**Slash commands don't show up**
- Set `GUILD_ID` in `.env` to your test server's ID — commands then appear instantly.
- Make sure you invited the bot with the **`applications.commands`** scope. If not,
  re-invite with a new OAuth2 URL.
- Fully close and reopen Discord (the list is cached).

**"This interaction failed"**
The code errored before replying. Check the terminal for the red traceback. The usual
culprit is a missing **`await`**, or replying twice to the same interaction.

**"Unknown interaction" / took too long**
You didn't respond within **3 seconds**. Call `await interaction.response.defer()` first for
slow commands, then `interaction.followup.send(...)`.

**`InteractionResponded` — already responded**
You called `interaction.response.send_message` twice. After the first response, use
`interaction.followup.send(...)` instead.

## Moderation & roles

**"Missing Permissions" when a command runs**
Discord is refusing the **bot**, not you. Two fixes:
- The bot's role must be **above** the member it's acting on — drag it up in Server Settings
  → Roles.
- The bot must actually have the permission — re-invite with the box checked.

**`/warn` couldn't DM the member**
Their DMs are closed. Expected — the warning still posts in the channel.

**A role won't get added**
The bot needs **Manage Roles**, and its role must sit **above** the role it's handing out.

## Components (buttons / dropdowns / modals)

**Buttons/dropdown stop working after a restart**
They're not persistent. Add `timeout=None`, a `custom_id` on every component, and
`self.bot.add_view(...)` in the cog's `cog_load`.

**"This interaction failed" on a button**
Same as commands — the callback errored (check the terminal) or didn't respond. A callback
must call `interaction.response.send_message(...)` (or `defer`, `edit_message`, `send_modal`).

## Data

**JSON `KeyError`**
You read a key that doesn't exist. Use `.get(key, default)` instead of `data[key]`, and
remember JSON keys are **strings** — use `str(user_id)`.

**Data resets every restart**
You're changing the dictionary in memory but never calling `save()`. Save after every
change.

**SQLite changes don't stick**
You forgot `conn.commit()` after an `INSERT`/`UPDATE`.

## Auto-moderation / message events

**`on_message` never fires**
The **Message Content Intent** is off (portal *and* code: `intents.message_content = True`).

**The bot reacts to its own messages / loops forever**
Always start message listeners with `if message.author.bot: return`.

**Prefix commands stopped working after I added on_message**
End your `on_message` with `await bot.process_commands(message)`.

## Still stuck?

1. Read the **terminal** — the traceback names the file and line.
2. Compare your file against the working version in the `bot/` folder.
3. Search the exact error text — you're rarely the first to hit it.
4. Check the official docs at **discordpy.readthedocs.io**.
