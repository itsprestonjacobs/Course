# Events

**Events** are the things that happen in a server that your bot can react to. You already
met two — `on_ready` and `on_message`. This lesson shows the pattern and the events you'll
use most.

## The pattern

Every event is a function decorated with `@bot.event`, named `on_something`, and defined
with `async def`:

```python
@bot.event
async def on_member_join(member):
    print(f"{member} joined the server!")
```

discord.py calls your function automatically when that thing happens, and hands you useful
info as arguments (here, the `member` who joined).

## The events you'll use most

| Event | Fires when… | You get |
|-------|-------------|---------|
| `on_ready` | the bot finishes logging in | *(nothing)* |
| `on_message` | any message is sent | the `message` |
| `on_member_join` | someone joins the server | the `member` |
| `on_member_remove` | someone leaves | the `member` |
| `on_message_delete` | a message is deleted | the `message` |
| `on_reaction_add` | someone reacts | the `reaction`, `user` |

## Example: a welcome message

```python
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel      # the server's default channel
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! 🎉")
```

`member.mention` produces a clickable @ping. `member.guild` is the server the member joined.
We build a full welcome system later — this is the seed.

## Example: reacting to keywords

```python
@bot.event
async def on_message(message):
    if message.author.bot:
        return                       # ignore all bots, including ourselves
    if "good bot" in message.content.lower():
        await message.add_reaction("❤️")
```

## The on_message gotcha

If you use `on_message` **and** prefix commands (`!hello`), your prefix commands stop working
unless you re-enable them at the end of the event:

```python
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # ... your custom logic ...
    await bot.process_commands(message)   # keep prefix commands alive
```

Since this course uses **slash commands** (which are separate and don't need this), you'll
rarely hit it — but now you know why it happens.

## Practice

Add a "goodbye" message when someone leaves:

```python
@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"{member.name} has left. 👋")
```

**Challenge:** make the bot react with 👀 whenever a message contains the word "bug".

<details><summary>Solution</summary>

```python
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if "bug" in message.content.lower():
        await message.add_reaction("👀")
```
</details>

## Recap

- Events are `@bot.event async def on_...(...)` functions the library calls for you.
- Key events: `on_ready`, `on_message`, `on_member_join/remove`, reactions.
- Always ignore bot messages (`if message.author.bot: return`).
- With prefix commands, end `on_message` with `await bot.process_commands(message)`.

→ **Next: Slash Commands**
