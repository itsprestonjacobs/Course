# Lesson 08 — Hosting & Next Steps

Your bot only runs while `python main.py` is running on your computer. Close the terminal
or shut down, and the bot goes offline. This lesson covers keeping it online 24/7 and where
to go from here.

## Option 1 — Run it on your own PC (free, simple)

Totally fine while you're learning and testing. Just know the bot is offline whenever your
computer is off or asleep. Nothing to set up beyond what you already have.

## Option 2 — A host that runs it 24/7

To keep the bot online all the time, it needs to live on a computer that never sleeps — a
**host**. The usual choices:

- **A VPS** (a small rented Linux server, e.g. from a budget provider) — the most reliable
  and what most serious bots use. Around a few dollars a month.
- **A bot-hosting service** — sites built specifically for hosting Discord bots. Easiest to
  start with; you upload your files and hit start.

The steps are similar everywhere:

1. Put your project on the host (upload the files, or push to GitHub and pull it down).
2. Install the requirements there:
   ```
   pip install -r requirements.txt
   ```
3. Add your token. On a host you usually set `DISCORD_TOKEN` as an **environment variable**
   in their dashboard instead of using a `.env` file — safer and the standard way.
4. Start it:
   ```
   python main.py
   ```
5. Keep it running after you log out. On a Linux VPS, a **systemd service** or a tool like
   `screen`/`tmux` keeps the process alive. Managed hosts do this for you.

> 🔒 **Never upload your `.env`** or your token to GitHub. Add a file called
> `.gitignore` containing the line `.env` so git skips it. If a token ever leaks, reset it
> in the Developer Portal immediately.

## The requirements.txt file

Any host needs to know which libraries to install. That's what `requirements.txt` is for:

```
discord.py>=2.3.2
python-dotenv>=1.0.0
```

Keep this file next to `main.py`. If you add a new library later, add it here too.

## Where to go next

You've got embeds, moderation, and a ticket system. Natural next features to try:

- **A welcome message** — greet new members with `@bot.event async def on_member_join`.
- **Reaction/button roles** — let members give themselves roles (you already know Views!).
- **A logging cog** — post to a mod-log channel when someone is kicked or banned.
- **Slash command groups** — organize commands like `/ticket open`, `/ticket close`.
- **A database** — store warnings so they persist. `sqlite3` (built into Python) is a great
  first database.

The official docs at **discordpy.readthedocs.io** are excellent, and the pattern you
learned — a cog with commands and a `setup` function — is how you'll add every one of the
features above.

## You did it 🎉

You started from installing Python and finished with a real, branded Discord bot running
the same kind of ticket panels Derpy's Designs uses. Rebrand it, extend it, and make it
yours.

← Back to the [Troubleshooting](troubleshooting.md) page if anything's still misbehaving.
