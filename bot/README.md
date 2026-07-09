# Derpy's Designs — Reference Bot

This is the **finished bot** students are building toward. Every code snippet in the
lessons comes from these files, so learners can always compare their work against it.

## Run it

1. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and paste your bot token (see Lesson 03 for how to get one).
3. Start the bot:
   ```
   python main.py
   ```
   You should see `Logged in as ...` in the terminal.

> **Tip:** Set `GUILD_ID` in your `.env` to your test server's ID. Slash commands then
> appear instantly instead of taking up to an hour to register globally.

## What's inside

| File | What it does |
|------|--------------|
| `main.py` | Starts the bot, loads the cogs, syncs slash commands |
| `cogs/embeds.py` | `/serverinfo`, `/announce` — building rich embeds |
| `cogs/moderation.py` | `/kick`, `/ban`, `/timeout`, `/purge`, `/warn` with permission checks |
| `cogs/tickets.py` | `/ticketpanel` + Open/Close buttons that create private ticket channels |

## Test checklist

Do this in a **test server you own** so you can't break anything real.

- [ ] Bot comes online (green dot) and the terminal prints `Synced N commands`.
- [ ] `/ping`-style embed: run `/serverinfo` — you get an embed with member/channel counts.
- [ ] `/announce title:Hello message:World` posts an embed.
- [ ] `/kick` on a test alt works; running it without the Kick Members permission is refused.
- [ ] `/timeout minutes:1` mutes a member for a minute.
- [ ] `/purge amount:5` deletes the last 5 messages.
- [ ] `/ticketpanel` posts the panel. Clicking **Open Ticket** creates a private
      `ticket-<id>` channel only you and Staff can see.
- [ ] Clicking **Close** deletes the channel (and drops a transcript in `#ticket-logs`
      if that channel exists).
- [ ] Restart the bot, then click **Open Ticket** again — it still works (persistent views).

## Server setup notes

- Create a role called **Staff** (or change `STAFF_ROLE_NAME` in `.env`) — that role can
  see and manage tickets.
- Optionally create a channel called **ticket-logs** to receive closed-ticket transcripts.
- The bot's own role must be **above** the members it moderates, or Discord will refuse
  the action. Drag it up in Server Settings → Roles.
