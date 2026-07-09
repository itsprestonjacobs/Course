# Async & Await

This is the one genuinely new idea in bot programming, so we give it its own lesson. Read
slowly — once it clicks, all the Discord code that follows will make sense.

## The problem it solves

A bot spends almost all its time **waiting** on the internet: waiting for a message,
waiting for Discord to create a channel, waiting for a reply to send. If the bot froze
solid every time it waited, it could only handle one thing at a time — one slow command
would block everyone else.

**Async** lets the bot start something slow, and while it waits, go handle other things.
It's like a waiter who takes your order and, instead of standing frozen at your table until
the kitchen is done, goes and serves other tables in the meantime.

## The two keywords

- **`async def`** marks a function that's *allowed to pause* while it waits.
- **`await`** is the pause point — "wait here for this to finish, then continue."

```python
async def open_ticket():
    channel = await guild.create_text_channel("ticket-1")
    await channel.send("Ticket opened!")
```

Read it as: *create the channel (wait for it), then send a message in it (wait for that).*

## The one rule you must remember

> Anything that talks to Discord needs `await` in front of it, and `await` can only be used
> inside a function defined with `async def`.

Almost every discord.py action — `send`, `kick`, `ban`, `create_text_channel`,
`response.send_message` — must be `await`ed.

## The most common beginner bug

If you forget `await`, the code **doesn't crash** — it just silently doesn't do the thing:

```python
channel.send("Hello!")          # ❌ nothing happens, no error
await channel.send("Hello!")    # ✅ actually sends
```

So when a command "runs but does nothing," a missing `await` is the very first thing to
check. Newer versions of Python may print a "coroutine was never awaited" warning to hint at
this.

## await gives you the result

`await` doesn't just pause — it also hands back whatever the action produced:

```python
message = await channel.send("Hello!")   # message is now the sent message object
await message.add_reaction("👍")          # ...which we can react to
```

## You won't write the loop yourself

There's an "event loop" running underneath that juggles all these paused functions. Good
news: discord.py starts and manages it for you. You just write `async def` functions and
sprinkle in `await` — the library handles the rest.

## Practice (concept check)

Which of these will actually send a message? (Assume we're inside an `async def`.)

```python
# A
channel.send("hi")

# B
await channel.send("hi")

# C
def helper():
    await channel.send("hi")
```

<details><summary>Answer</summary>

- **A** — no, missing `await`; nothing happens.
- **B** — yes ✅.
- **C** — no; it's a syntax error, because `await` is inside a plain `def`, not an
  `async def`.
</details>

## Recap

- Bots wait a lot; **async** lets them stay responsive while waiting.
- `async def` = a pausable function; `await` = the pause that also returns a result.
- **Rule:** Discord actions need `await`, inside an `async def`.
- Forgot `await`? The action silently does nothing — check this first.

🎉 **That's all the Python you need.** From here on it's all Discord. Next we bring your bot
to life.

→ **Next: Register Your Bot**
