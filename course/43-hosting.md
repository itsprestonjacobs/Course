# Host It 24/7

Your bot only runs while `python main.py` is running on your computer. Close the terminal or
shut down, and it goes offline. To keep it online around the clock, it needs to live on a
computer that never sleeps — a **host**.

## Step 1 — A requirements file

Any host needs to know which libraries to install. List them in `requirements.txt` next to
`main.py`:

```
discord.py>=2.3.2
python-dotenv>=1.0.0
aiohttp
```

Add any other library you `pip install`ed. On the host you'll run
`pip install -r requirements.txt` to get them all at once.

## Option A — Run on your own PC (free)

Totally fine while learning. The bot is online only while your computer is on and the script
is running. Nothing extra to set up.

## Option B — A VPS (the standard for real bots)

A **VPS** is a small rented Linux computer that stays on 24/7 (a few dollars a month). The
steps once you have one:

1. **Get your code there.** Easiest: push to GitHub (last lesson), then on the server run
   `git clone https://github.com/you/your-repo.git`.
2. **Install Python and the requirements:**
   ```
   pip install -r requirements.txt
   ```
3. **Add your token.** On a server, set it as an **environment variable** instead of a
   `.env` file (safer and standard). How you do this depends on the host; often it's a
   dashboard field or an `export DISCORD_TOKEN=...` line.
4. **Keep it running after you log out.** If you just run `python main.py` and disconnect,
   it stops. Use one of these:

### Keep-alive with a systemd service (recommended on Linux)

Create `/etc/systemd/system/mybot.service`:

```
[Unit]
Description=My Discord Bot
After=network.target

[Service]
WorkingDirectory=/home/youruser/your-repo
ExecStart=/usr/bin/python3 main.py
Restart=always
Environment=DISCORD_TOKEN=your-token-here

[Install]
WantedBy=multi-user.target
```

Then:

```
sudo systemctl enable mybot     # start on boot
sudo systemctl start mybot      # start now
sudo systemctl status mybot     # check it's running
```

`Restart=always` means if the bot crashes, the server restarts it automatically. That's the
big win of systemd.

### The quick-and-dirty way

For testing, `screen` or `tmux` keeps a session alive after you disconnect:

```
screen -S bot
python3 main.py
# press Ctrl+A then D to "detach" and leave it running
```

## Option C — A managed bot host

Several services are built specifically to host Discord bots: you connect your GitHub repo
(or upload files), set your token in their dashboard, and click start. They handle keeping it
alive for you. Easiest to begin with; search "Discord bot hosting" and compare.

## A note on "free" hosts that sleep

Some free hosting tiers put your app to sleep when idle, which kills a bot. Bots need to stay
connected constantly, so pick a host that runs your process continuously (a proper VPS or a
bot-specific host), not one meant only for websites.

## Practice

**Checklist before you deploy:**

- [ ] `requirements.txt` lists every library you use.
- [ ] The token is set as an environment variable on the host (not committed to GitHub).
- [ ] `Restart=always` (or the host's equivalent) is on, so a crash auto-recovers.
- [ ] You tested that the bot reconnects after the host reboots.

## Recap

- A **host** keeps your bot online 24/7; list dependencies in `requirements.txt`.
- On a **VPS**, use a **systemd service** with `Restart=always` so it survives crashes and
  reboots.
- Set the token via an **environment variable**, never in the repo.
- Avoid free tiers that sleep idle apps.

→ **Next: Wrap-up & Next Steps**
