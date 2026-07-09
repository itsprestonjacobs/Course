# Lesson 02 — Python Crash Course

You don't need to master Python to build a bot — you need maybe six ideas. This is all of
them. Make a file called `practice.py` in your project and try each snippet by running
`python practice.py`.

## Printing and variables

`print()` shows text. A **variable** is a labeled box that stores a value.

```python
name = "Derpy"
age = 3
print("Hello", name)
print(name, "is", age, "years old")
```

## f-strings (the clean way to build text)

Put an `f` before the quotes and drop variables straight into the string with `{ }`:

```python
name = "Derpy"
print(f"Hello {name}, welcome back!")
```

We use f-strings constantly in the bot for things like `f"ticket-{author.id}"`.

## Functions

A **function** is a reusable chunk of code you give a name. You "call" it to run it.

```python
def greet(who):
    print(f"Hi {who}!")

greet("Sam")
greet("Alex")
```

`who` is an **argument** — a value you hand the function to work with.

## Imports

Most code you use is written by other people. `import` pulls it in:

```python
import discord
```

Now you can use everything the `discord` library offers.

## if / else — making decisions

```python
members = 120
if members > 100:
    print("Big server!")
else:
    print("Cozy server.")
```

The bot uses this everywhere, e.g. "if this person already has a ticket, don't make a new
one."

## async and await — the one new idea

This is the only unusual part, so read slowly. A Discord bot is constantly waiting on the
internet: waiting for a message, waiting for Discord to create a channel, waiting for a
reply. If the bot froze every time it waited, it could only do one thing at a time.

**`async`** marks a function that's allowed to pause and let other work happen while it
waits. **`await`** is where it pauses until an answer comes back.

```python
async def open_ticket():
    channel = await guild.create_text_channel("ticket-1")
    await channel.send("Ticket opened!")
```

You don't need to fully understand *how* it works. Just remember the rule:

> Bot actions that talk to Discord almost always need `await` in front of them, and they
> must live inside a function defined with `async def`.

If you forget an `await`, the code won't crash loudly — it just won't do the thing. So
when a command "does nothing," a missing `await` is the first thing to check.

## That's genuinely enough

Variables, f-strings, functions, imports, if/else, and async/await. With those six ideas
the bot code will read like plain instructions. On to the fun part — making the bot exist.

→ **Lesson 03: Register your bot**
