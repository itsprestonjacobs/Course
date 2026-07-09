# Invite Your Bot

Your bot exists but isn't in any server yet. Let's build an invite link and add it to your
test server.

## Step 1 — Open the URL Generator

In your app on the developer portal, go to **OAuth2 → URL Generator** in the left menu.

## Step 2 — Choose scopes

Under **Scopes**, tick two boxes:

- **`bot`** — lets you add it as a bot.
- **`applications.commands`** — lets it register slash commands.

> ⚠️ If you forget **`applications.commands`**, your slash commands will never show up. This
> is one of the most common "my commands don't appear" causes.

## Step 3 — Choose permissions

A **Bot Permissions** box appears below. Tick the ones from the last lesson:

- Manage Channels
- Manage Roles
- Kick Members
- Ban Members
- Moderate Members
- Manage Messages
- Send Messages
- Embed Links
- Read Message History

> 💡 Only grant what you need. It's tempting to tick **Administrator**, but that's a security
> risk — if your bot is ever compromised, Administrator gives an attacker the whole server.

## Step 4 — Use the link

1. Copy the **Generated URL** at the very bottom.
2. Paste it into your browser.
3. Choose your test server from the dropdown, click **Authorize**, and solve the captcha.

Your bot now appears in the server's member list — offline for now, because we haven't
written the code that logs it in. That's the very next lesson.

## Step 5 — Fix the role order (do this now)

In **Server Settings → Roles**, drag your bot's role **near the top** of the list. A bot can
only kick, ban, or timeout members whose highest role sits **below** its own. Setting this
now saves a confusing "Missing Permissions" error later.

## Re-inviting later

Need to add a permission or the `applications.commands` scope you forgot? Just generate a
new URL with the right boxes ticked and open it again — it updates the existing bot, no need
to remove it first.

## Recap

- Built an invite with the **`bot`** + **`applications.commands`** scopes.
- Granted the permissions the course needs (avoid Administrator).
- **Authorized** it into your test server.
- Dragged the bot's role up so moderation works.

→ **Next: First Connection**
