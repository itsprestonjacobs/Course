# Troubleshooting

Almost every beginner hits the same handful of errors. Find yours here before pulling your
hair out.

## The bot won't start

**`No token found` / `LoginFailure: Improper token`**
Your token is missing or wrong. Check that:
- You have a file named exactly `.env` (not `env.txt`) next to `main.py`.
- The line reads `DISCORD_TOKEN=...` with your real token and no quotes or spaces.
- The token hasn't been reset. If unsure, reset it in the Developer Portal and paste the
  new one.

**`ModuleNotFoundError: No module named 'discord'`**
The library isn't installed in the environment you're running. Make sure `(venv)` shows in
your terminal, then run `pip install discord.py python-dotenv` again.

**`python` is not recognized**
Python isn't on your PATH. Reinstall Python and check **"Add Python to PATH"** on the first
installer screen.

**Windows: "running scripts is disabled on this system"**
Run this once, then activate the venv again:
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## The bot is online but…

**Slash commands don't show up**
- Set `GUILD_ID` in your `.env` to your test server's ID — commands then appear instantly.
  Without it, global commands can take up to an hour.
- Make sure you invited the bot with the **`applications.commands`** scope (Lesson 03). If
  not, re-invite it with a new OAuth2 URL.
- Fully close Discord and reopen it; the command list is cached.

**`PrivilegedIntentsRequired` on startup**
You didn't flip the intent switches. In the Developer Portal → your app → **Bot**, turn on
**Server Members** and **Message Content**, then Save.

**A command replies "This interaction failed"**
Usually the code errored before replying. Look at your terminal for the red traceback — it
names the file and line. A very common cause is forgetting `await` in front of a Discord
action.

## Moderation problems

**"Missing Permissions" when a command runs**
Discord is refusing the **bot**, not you. Two fixes:
- The bot's role must be **above** the member it's acting on. Drag it up in Server Settings
  → Roles.
- The bot must actually have the permission (Kick/Ban/etc.). Re-invite it with those boxes
  checked, or grant the permission to its role.

**`/warn` says it couldn't DM the member**
That member has DMs turned off. Nothing you can do — the warning embed still posts in the
channel.

## Ticket problems

**Clicking the dropdown/Close does nothing after a restart**
You need the persistence step. Make sure the `cog_load` method with `self.bot.add_view(...)`
is in your `Tickets` cog (Lesson 07, Step 6), and that every button/dropdown has a
`custom_id`.

**Ticket channel is visible to everyone**
Check the permission overwrites in `create_ticket` — `guild.default_role` must be set to
`view_channel=False`.

**No transcript appears on close**
The transcript is only saved if a channel named exactly `ticket-logs` exists. Create it, or
remove that part of the code.

## Still stuck?

Read the **terminal output** — the actual error message almost always names the file and
line number. Copy the last few red lines and search them; you're rarely the first person to
hit that exact error.
