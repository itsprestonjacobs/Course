# How Discord Bots Work

Before we write a single line of code, let's understand what a bot actually *is*. Five
minutes here saves you hours of confusion later.

## A bot is just a program pretending to be a user

When you log into Discord, an app on your phone or computer talks to Discord's servers over
the internet. A **bot** does the exact same thing — except instead of a person clicking
buttons, it's a **Python program** making the decisions. That program logs in with its own
account (a "bot account"), listens for things happening, and reacts.

So a bot is really just: *log in → wait for something to happen → do something about it.*

## The two halves: events and actions

Everything a bot does falls into one of two buckets.

- **Events** — things that *happen* that your bot hears about. A message was sent. A member
  joined. Someone clicked a button. Discord pushes these to your bot in real time.
- **Actions** — things your bot *does* in response. Send a message. Kick a member. Create a
  channel. Your bot asks Discord to do these.

The whole course is really just learning which events you can listen to and which actions
you can take.

## The gateway and the API

Two words you'll see everywhere:

- The **Gateway** is the live connection where Discord streams events to your bot. Think of
  it as your bot's ears — it's how the bot hears "a message just arrived."
- The **API** (Application Programming Interface) is how your bot sends requests back —
  "please send this message," "please ban this user." Think of it as your bot's hands.

You will almost never touch these directly. A library called **discord.py** wraps both of
them in friendly Python, so you write `await member.kick()` and it handles the messy
internet stuff underneath.

## What you'll actually type

A tiny bot, in plain terms, looks like this:

```
when the bot is ready:
    print "I'm online!"

when a message is sent:
    if the message says "hello":
        reply "hi there!"
```

That's the whole mental model. By the end of this course you'll write exactly that — plus
embeds, moderation, buttons, a database, and more — in real Python.

## Slash commands

Modern bots are mostly controlled with **slash commands** — you type `/` in Discord and
pick a command from a menu (like `/ban` or `/serverinfo`). Discord shows the list, checks
who's allowed to use each one, and even gives users fill-in boxes for the inputs. We'll use
slash commands throughout because they're the standard and they're beginner-friendly.

## What you need

- **Python** — the language your bot is written in.
- **A code editor** (VS Code) — where you write the code.
- **A Discord account and a test server** — your bot's playground.
- **discord.py** — the library that does the heavy lifting.

Next lesson we install all of it.

## Recap

- A bot is a Python program logged in as its own account.
- It **listens for events** and **takes actions**.
- The **Gateway** delivers events; the **API** sends actions; **discord.py** wraps both.
- We'll control the bot with **slash commands**.

→ **Next: Install Your Tools**
