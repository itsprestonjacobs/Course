# Host It 24/7

Your bot only runs while `python main.py` is running somewhere. Close the terminal and it
goes offline. This lesson covers the two easiest ways to keep it online: **self-hosting on
your own PC**, and a **free bot host (hollow.host)** that runs it 24/7 for you.

## First: the requirements file

Any host — including your own PC — needs to know which libraries to install. List them in
`requirements.txt` next to `main.py`:

```
discord.py>=2.3.2
python-dotenv>=1.0.0
aiohttp>=3.9.0
```

Add any other library you `pip install`ed. Installing them anywhere is then one command:
`pip install -r requirements.txt`.

---

## Option A — Self-host on your own PC

The simplest option: run the bot on your own computer. Free, no accounts, full control.

### Steps

1. Open your project in VS Code and open the terminal.
2. Activate your virtual environment (`venv\Scripts\Activate` on Windows).
3. Run it:
   ```
   python main.py
   ```
4. **Leave that terminal open.** As long as it's running and your PC is on, the bot is
   online.

### Keep it from going offline

Self-hosting has one catch — the bot is offline whenever your PC is **off** or **asleep**.
To keep it up:

- **Stop the PC sleeping:** Windows **Settings → System → Power → Screen and sleep** → set
  "When plugged in, put my device to sleep" to **Never**.
- **Don't close the terminal** or shut down while you want the bot online.

### Auto-start when your PC boots (Windows, optional)

So you don't have to launch it by hand every time:

1. Make a file called `run_bot.bat` in your project folder with these lines:
   ```
   @echo off
   cd /d "%~dp0"
   call venv\Scripts\activate
   python main.py
   ```
2. Press **Win + R**, type `shell:startup`, press Enter — this opens your Startup folder.
3. Right-click `run_bot.bat` → **Create shortcut**, and move the shortcut into that Startup
   folder.

Now the bot launches automatically whenever you log into Windows.

> **When self-hosting is fine:** while you're learning and testing, or for a small server
> where a little downtime is OK. For a bot lots of people rely on, use a real host (below)
> so it stays up even when your PC is off.

---

## Option B — Free 24/7 hosting with hollow.host

[hollow.host](https://hollow.host/) is a free Discord-bot host that keeps your bot online
around the clock on their servers, so it doesn't depend on your PC. Like most free bot
hosts, it gives you a **web control panel** where you upload your code, set your token, and
click Start.

### Steps

1. **Sign up** at [hollow.host](https://hollow.host/) and create a bot server/instance.
   Many free hosts have you sign in with Discord and "claim" a free server through their
   support Discord — check their site/Discord for the exact claim step.
2. **Choose Python.** When it asks what kind of app you're running, pick the **Python** type
   (sometimes called an "egg" or image).
3. **Upload your files.** Use the panel's **File Manager** to upload your project — or, even
   easier, connect the **GitHub repo** you made last lesson so it pulls your code. Upload
   everything *except* your `.env` and `venv` folder.
4. **Set your token safely.** In the panel's **Startup** or **Variables** section, add an
   environment variable named `DISCORD_TOKEN` with your token as the value. This replaces
   the `.env` file — never upload the `.env` itself.
5. **Set the startup command** to run your bot and install requirements. It's usually
   something like:
   ```
   pip install -r requirements.txt && python main.py
   ```
   Many panels install `requirements.txt` automatically — if so, the start command is just
   `python main.py`.
6. **Click Start.** Watch the panel's **Console** — you should see your familiar
   `Logged in as …` and `Synced N commands`. Your bot is now online 24/7. 🎉

> The panel labels above (File Manager, Startup, Variables, Console) are the standard ones
> most free bot hosts use, but hollow.host may name them slightly differently. If you get
> stuck, their support Discord (linked on their site) will have the exact steps.

### Reading your token from an environment variable

Good news: **your bot already supports this.** `main.py` uses
`os.getenv("DISCORD_TOKEN")`, which reads either your local `.env` file *or* an environment
variable set on the host. So no code changes are needed — set `DISCORD_TOKEN` in the panel
and it just works.

---

## Advanced — a VPS with auto-restart

If you outgrow free hosting, a **VPS** (a small rented Linux server, a few dollars a month)
gives you full control. Clone your GitHub repo onto it, install requirements, set the token
as an environment variable, and run it under a **systemd service** with `Restart=always` so
it auto-recovers from crashes and reboots. This is how large bots run, but it's optional —
hollow.host is plenty to start.

## A note on hosts that "sleep"

Some free tiers meant for websites put your app to sleep when it's idle, which kills a bot
(bots must stay connected constantly). Bot-specific hosts like hollow.host are built to keep
your process running non-stop — that's exactly what you want.

## Deploy checklist

- [ ] `requirements.txt` lists every library you use.
- [ ] Your token is set as an environment variable on the host (or `.env` locally) — **never**
      uploaded to GitHub.
- [ ] The console shows `Logged in as …` and `Synced N commands`.
- [ ] The bot reconnects after the host (or your PC) restarts.

## Recap

- List your libraries in **`requirements.txt`**.
- **Self-host** by running `python main.py` on your PC (stop it sleeping; auto-start with a
  `.bat` in the Startup folder) — great for learning.
- For true 24/7, use a free bot host like **hollow.host**: upload your code (or connect
  GitHub), set `DISCORD_TOKEN` as an environment variable, set the start command, and hit
  Start. Your `main.py` already reads the token from the environment, so no code changes.

→ **Next: Wrap-up & Next Steps**
