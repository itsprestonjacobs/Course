# Install Your Tools

Let's get Python and VS Code installed and a project folder ready. Follow every step in
order — a lot of "my bot won't run" problems trace back to a skipped step here.

## Step 1 — Install Python

1. Go to **python.org/downloads** and click the big **Download Python** button.
2. Run the installer.
3. **CRUCIAL:** on the first screen, tick **"Add Python to PATH"** at the bottom. Miss this
   and the `python` command won't work.
4. Click **Install Now** and let it finish.

> ✅ **Check it.** Open a terminal (Windows: press Start, type `powershell`, Enter) and run
> `python --version`. You should see `Python 3.12.x` or similar.

## Step 2 — Install VS Code

1. Go to **code.visualstudio.com** and download **Visual Studio Code**.
2. Install it with the default options.
3. Open it, click the **Extensions** icon on the left (four squares), search **Python**,
   and install the one by **Microsoft**.

## Step 3 — Terminal basics (30-second crash course)

The **terminal** is where you type commands. You only need three:

- `cd foldername` — go *into* a folder (change directory).
- `cd ..` — go *back up* one folder.
- `dir` (Windows) / `ls` (Mac/Linux) — list what's in the current folder.

That's genuinely all you need for this whole course.

## Step 4 — Make your project folder

1. Make a new folder somewhere easy, like `Documents\discord-bot`.
2. In VS Code: **File → Open Folder**, and select it.
3. Open the terminal inside VS Code: **Terminal → New Terminal**. Everything from now on
   gets typed here.

## Step 5 — Create a virtual environment

A **virtual environment** is a private box for this project's libraries, so they don't
clash with anything else on your computer. In the VS Code terminal:

```
python -m venv venv
```

Then turn it on:

```
# Windows (PowerShell)
venv\Scripts\Activate

# Mac / Linux
source venv/bin/activate
```

You'll know it worked when the line starts with `(venv)`.

> ⚠️ **Windows blocked the script?** If you see "running scripts is disabled", run this
> once, then activate again:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Step 6 — Install discord.py

With `(venv)` showing:

```
pip install discord.py python-dotenv
```

- **discord.py** is the bot library.
- **python-dotenv** lets us keep our secret token in a file instead of in the code.

> ✅ **Check it.** Run `pip list` — `discord.py` should appear in the list.

## Practice

Run these to prove your setup works:

```
python --version
pip list
```

If both run without errors and you see `discord.py`, you're ready. If not, the
**Troubleshooting** page has fixes for every common setup error.

## Recap

- Installed **Python** (with "Add to PATH") and **VS Code** (+ Python extension).
- Learned `cd`, `cd ..`, and `ls`/`dir`.
- Made a project folder and a **virtual environment** (`venv`).
- Installed **discord.py** and **python-dotenv**.

→ **Next: Python — Variables & Types**
