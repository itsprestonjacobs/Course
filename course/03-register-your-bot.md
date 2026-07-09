# Lesson 03 — Register Your Bot

Right now your bot doesn't exist to Discord. In this lesson we create its account, get its
secret **token** (like a password), and invite it into a server. No code yet — this all
happens on Discord's website.

## Step 1 — Make a test server

If you don't already have a server to mess around in, make one. In Discord click the **+**
on the left → **Create My Own** → give it any name. You're the owner, so you can't break
anything important.

## Step 2 — Create an application

1. Go to **discord.com/developers/applications** and log in.
2. Click **New Application** (top right), name it (e.g. "Derpy Bot"), agree, and **Create**.
3. This "application" is the container for your bot.

## Step 3 — Turn it into a bot and get the token

1. In the left menu click **Bot**.
2. Under **Token**, click **Reset Token** → **Yes, do it** → **Copy**.
3. Paste it somewhere safe for a minute. We'll put it in a file next lesson.

> 🔒 **Treat the token like a password.** Anyone who has it can control your bot. Never
> post it in Discord, never put it on GitHub. If it ever leaks, come back here and click
> **Reset Token** — the old one instantly stops working.

## Step 4 — Turn on the intents

Scroll down on the same **Bot** page to **Privileged Gateway Intents** and switch ON:

- **Server Members Intent**
- **Message Content Intent**
- **Presence Intent** (optional, but turn it on so nothing surprises you later)

**Intents** are permissions for what kinds of events your bot is allowed to receive.
Our moderation and ticket features need to know about members, so these must be on. Click
**Save Changes**.

## Step 5 — Build the invite link

1. In the left menu open **OAuth2 → URL Generator**.
2. Under **Scopes**, check **`bot`** and **`applications.commands`**
   (that second one is what makes slash commands work).
3. A **Bot Permissions** box appears below. Check these:
   - Manage Channels
   - Kick Members
   - Ban Members
   - Moderate Members
   - Manage Messages
   - Send Messages
   - Read Message History
   - Embed Links
4. Copy the **generated URL** at the very bottom.

## Step 6 — Invite the bot

Paste that URL into your browser, pick your test server, click **Authorize**, solve the
captcha. Your bot now shows up in the member list — offline for now, because we haven't
written the code that logs it in. That's next.

> 💡 **Role order matters.** In **Server Settings → Roles**, drag your bot's role near the
> top. A bot can only kick/ban/timeout members whose highest role is **below** its own.

→ **Lesson 04: Your first bot**
