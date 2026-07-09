# Lesson 01 — Setup

Before we write any bot code we need two free tools: **Python** (the language) and **VS
Code** (where we write and run the code). This lesson gets both installed and your project
folder ready.

## Step 1 — Install Python

1. Go to **python.org/downloads** and click the big yellow **Download Python** button.
2. Run the installer.
3. **VERY IMPORTANT:** on the first screen, check the box that says
   **"Add Python to PATH"** at the bottom. If you miss this, the `python` command won't
   work later.
4. Click **Install Now** and let it finish.

> ✅ **Check it worked.** Open a terminal (on Windows press the Start key, type
> `powershell`, hit Enter) and run:
> ```
> python --version
> ```
> You should see something like `Python 3.12.4`. If you get an error, Python wasn't added
> to PATH — reinstall and make sure that box is checked.

## Step 2 — Install VS Code

1. Go to **code.visualstudio.com** and download **Visual Studio Code**.
2. Install it (the defaults are fine).
3. Open VS Code, click the **Extensions** icon on the left (four squares), search for
   **Python**, and install the one by Microsoft. This gives you nice colors and error
   hints.

## Step 3 — Make your project folder

1. Make a new folder somewhere easy to find, like `Documents\discord-bot`.
2. In VS Code choose **File → Open Folder** and pick it.
3. Open the built-in terminal with **Terminal → New Terminal**. Everything from here on
   gets typed into this terminal.

## Step 4 — Create a virtual environment

A "virtual environment" is a private box for this project's libraries so they don't clash
with anything else on your computer. Run this in the VS Code terminal:

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

You'll know it worked when you see `(venv)` at the start of your terminal line.

> ⚠️ **Windows blocked the script?** If you see a red error about "running scripts is
> disabled", run this once, then try activating again:
> ```
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

## Step 5 — Install discord.py

With `(venv)` showing, install the library that talks to Discord:

```
pip install discord.py python-dotenv
```

`discord.py` is the bot library. `python-dotenv` lets us keep our secret token in a file
instead of pasting it into the code.

> ✅ **Check it worked.** Run `pip list` — you should see `discord.py` in the list.

## You're set up!

You now have Python, VS Code, a project folder, a virtual environment, and the library.
Next we'll learn just enough Python to understand what we're about to write.

→ **Lesson 02: Python crash course**
