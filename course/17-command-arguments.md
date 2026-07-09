# Command Arguments

Most commands need input: *who* to ban, *how many* messages to delete, *what* to say.
Slash commands make this beautiful — Discord builds fill-in boxes for you automatically.

## Adding an argument

Add a parameter to your command function, with a **type hint** after the colon:

```python
@bot.tree.command(description="Repeat what you say.")
async def echo(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(text)
```

`text: str` tells Discord this command takes a piece of text. When someone types `/echo`,
Discord shows a `text` box to fill in.

## Argument types

The type hint controls what Discord accepts:

```python
async def example(
    interaction: discord.Interaction,
    word: str,                       # text
    amount: int,                     # whole number
    rate: float,                     # decimal number
    enabled: bool,                   # true / false toggle
    member: discord.Member,          # a member picker
    channel: discord.TextChannel,    # a channel picker
    role: discord.Role,              # a role picker
):
    ...
```

The `discord.Member`, `discord.TextChannel`, and `discord.Role` types are the magic ones —
Discord gives users a proper picker instead of making them type an ID.

## Describing arguments

Add hints under each box with `@app_commands.describe`:

```python
from discord import app_commands

@bot.tree.command(description="Greet a member.")
@app_commands.describe(member="Who to greet", times="How many times")
async def greet(interaction: discord.Interaction, member: discord.Member, times: int):
    await interaction.response.send_message(f"{member.mention} " * times)
```

## Optional arguments

Give an argument a default value to make it optional:

```python
@bot.tree.command(description="Kick a member.")
@app_commands.describe(member="Who to kick", reason="Why (optional)")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await interaction.response.send_message(f"Would kick {member} — {reason or 'no reason'}")
```

`reason: str = None` means the user can skip it. Required arguments must come **before**
optional ones.

## Choices — a fixed menu of options

When you want the user to pick from a set list, use `choices`:

```python
@bot.tree.command(description="Set your status.")
@app_commands.describe(mood="How you're feeling")
@app_commands.choices(mood=[
    app_commands.Choice(name="Happy", value="happy"),
    app_commands.Choice(name="Busy", value="busy"),
    app_commands.Choice(name="Away", value="away"),
])
async def status(interaction: discord.Interaction, mood: app_commands.Choice[str]):
    await interaction.response.send_message(f"Status set to **{mood.value}**.")
```

Now Discord shows a dropdown with exactly those three options — no typos possible.

## Practice

Write a `/say` command that takes a `channel` and a `message`, and sends the message to that
channel:

```python
@bot.tree.command(description="Send a message to a channel.")
@app_commands.describe(channel="Where to send", message="What to send")
async def say(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    await channel.send(message)
    await interaction.response.send_message(f"Sent to {channel.mention}!", ephemeral=True)
```

**Challenge:** make a `/roll` command that takes an `int` called `sides` and replies with a
random number from 1 to `sides`. (Hint: `import random` and `random.randint(1, sides)`.)

<details><summary>Solution</summary>

```python
import random

@bot.tree.command(description="Roll a die.")
async def roll(interaction: discord.Interaction, sides: int):
    result = random.randint(1, sides)
    await interaction.response.send_message(f"🎲 You rolled a **{result}**!")
```
</details>

## Recap

- Add arguments as function parameters with **type hints** (`text: str`, `member: discord.Member`).
- `@app_commands.describe(...)` labels each box; a default value makes an argument optional.
- `@app_commands.choices(...)` gives a fixed dropdown of options.

→ **Next: Organizing with Cogs**
