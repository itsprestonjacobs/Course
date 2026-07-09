# Intents & Permissions

Two different ideas that beginners constantly mix up. Get them straight now and you'll skip
the two most common "why doesn't my bot work" problems.

## Intents — what your bot is allowed to *hear*

**Intents** control which events Discord sends your bot. By default a bot doesn't receive
message content or member updates — you have to opt in. This protects users' privacy and
keeps bots efficient.

### Turn on the privileged intents

On your app's **Bot** page (developer portal), scroll to **Privileged Gateway Intents** and
switch ON:

- **Server Members Intent** — so the bot hears about members joining/leaving (needed for
  welcome messages, moderation, tickets).
- **Message Content Intent** — so the bot can read message text (needed for auto-moderation
  and leveling).
- **Presence Intent** — optional; turn it on so nothing surprises you later.

Click **Save Changes**. If you forget this, your bot will crash on startup with a
`PrivilegedIntentsRequired` error — a rite of passage every bot dev hits once.

### Matching them in code (preview)

Whatever you switch on here, you also declare in your code:

```python
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
```

The website switch and the code line must **both** be on. Think of it as two locks on the
same door.

## Permissions — what your bot is allowed to *do*

**Permissions** are separate. They control the *actions* your bot can take in a server:
send messages, kick members, manage channels, and so on. Permissions are granted when you
invite the bot (next lesson) and can be adjusted per-channel in Discord.

The permissions our bot needs across the course:

| Permission | Used for |
|------------|----------|
| Send Messages / Embed Links | replying, embeds |
| Read Message History | transcripts, purge |
| Manage Channels | ticket system |
| Kick / Ban Members | moderation |
| Moderate Members | timeouts (mute) |
| Manage Messages | purge/clear |
| Manage Roles | auto-roles, reaction roles |

## Intents vs permissions — the one-line summary

- **Intents** = what the bot can *hear* (events Discord sends it).
- **Permissions** = what the bot can *do* (actions Discord lets it take).

Two things fail loudly when misconfigured: missing intents → crash on startup; missing
permissions → "Missing Permissions" when a command runs. We'll hit both later and you'll
know exactly which is which.

## Recap

- **Intents** opt your bot into events; turn on **Server Members** + **Message Content** in
  the portal *and* in code.
- **Permissions** control what the bot can do; granted at invite time.
- Different problems: intents → startup crash, permissions → action refused.

→ **Next: Invite Your Bot**
