# Git & GitHub for Your Bot

Before you host your bot, you want your code backed up and versioned. **Git** tracks changes
to your code; **GitHub** stores it online. This is how you avoid "I broke everything and
can't undo it," and it's the easiest way to get your bot onto a host later.

## Why bother

- **Backup** — your code lives safely in the cloud, not just on your laptop.
- **History** — every save (a "commit") is a snapshot you can roll back to.
- **Deployment** — most hosts pull your code straight from GitHub.

## Step 1 — Install Git

Download from **git-scm.com** and install with the defaults. Check it worked:

```
git --version
```

## Step 2 — Protect your token first

**This is the most important step.** Your `.env` holds your token and must **never** go to
GitHub. Make a file called `.gitignore` in your project with:

```
.env
__pycache__/
*.db
venv/
```

This tells Git to ignore those files. Your token, your database, and your virtual
environment stay local.

> 🔒 If you ever accidentally push your token, treat it as leaked: reset it in the Developer
> Portal immediately. Removing it from GitHub later isn't enough — bots scan public repos for
> tokens within seconds.

## Step 3 — Create the repository

In your project folder's terminal:

```
git init
git add .
git commit -m "Initial commit: my Discord bot"
```

- `git init` starts tracking this folder.
- `git add .` stages all your files (except the ignored ones).
- `git commit -m "..."` saves a snapshot with a message.

## Step 4 — Put it on GitHub

1. On **github.com**, click **New** to create a repository (name it, keep it **Private** if
   you like).
2. GitHub shows you commands to connect and push. They look like:

```
git remote add origin https://github.com/yourname/your-repo.git
git branch -M main
git push -u origin main
```

Refresh the GitHub page — your code is online.

## Step 5 — Saving changes going forward

Every time you make progress, save it:

```
git add .
git commit -m "Add economy system"
git push
```

Three commands, and your latest work is backed up. Do it often — small, frequent commits
are easier to understand than one giant one.

## A quick sanity check

After pushing, **look at your repository on GitHub and confirm `.env` is NOT there.** If you
see it, your token is exposed — reset it and fix your `.gitignore`.

## Practice

**Challenge:** make a small change (add a comment to `main.py`), then commit and push it with
a clear message.

<details><summary>Solution</summary>

```
git add .
git commit -m "Add a comment explaining the intents"
git push
```
</details>

## Recap

- **Git** versions your code; **GitHub** backs it up online.
- **Always** add `.env`, `*.db`, `venv/`, and `__pycache__/` to `.gitignore` first.
- Workflow: `git add .` → `git commit -m "..."` → `git push`.
- Verify your token file never made it to GitHub.

→ **Next: Host It 24/7**
