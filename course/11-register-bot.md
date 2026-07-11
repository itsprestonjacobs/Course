# Register Your Bot

Your bot doesn't exist to Discord yet. In this lesson we create its account and get its
secret **token**. This all happens on Discord's website — no code.

## Step 1 — Make a test server

If you don't have a server to experiment in, make one: click the **+** on the left in
Discord → **Create My Own** → name it anything. You're the owner, so you can't break
anything important.

## Step 2 — Create an application

1. Go to **discord.com/developers/applications** and log in.
2. Click **New Application** (top right).
3. Name it (e.g. "My Bot"), agree to the terms, and click **Create**.

This "application" is the container that will hold your bot.

## Step 3 — Turn it into a bot and copy the token

1. In the left menu, click **Bot**.
2. Find the **Token** section and click **Reset Token** → **Yes, do it** → **Copy**.
3. Paste it somewhere safe for a minute. Next lesson-block we'll put it in a file.

> 🔒 **Your token is a password.** Anyone who has it can fully control your bot — send
> messages, ban people, everything. **Never** paste it in a Discord chat, screenshot it, or
> upload it to GitHub. If it ever leaks, come back here and click **Reset Token**; the old
> one dies instantly.

## Step 4 — Give your bot a face (optional but nice)

While you're on this page, set the bot's **username** and **avatar** (icon). This is what
members see in the member list. You can rebrand it any time.

## What's a token, really?

When your Python code connects to Discord, it has to prove *which* bot it is. The token is
that proof — a long random string unique to your bot. Your code will read it from a file
and hand it to discord.py, which uses it to log in.

## Recap

- Created a Discord **application** and turned on its **Bot**.
- Copied the bot **token** (its password) and stored it safely.
- Next we'll set the **intents** and **permissions** that decide what the bot can do.

→ **Next: Intents & Permissions**
