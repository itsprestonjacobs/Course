# Saving Data with JSON

Right now, everything your bot knows disappears when it restarts. Warnings, coins, settings
— gone. To *remember* things, the bot needs to save them to a file. The simplest way is
**JSON**, and it's perfect for small-to-medium bots.

## The problem, concretely

```python
warnings = {}     # this dictionary lives only while the bot is running

warnings[123] = 2
# ...bot restarts...
print(warnings)   # {} — everything's gone
```

We need to **save** the dictionary to disk and **load** it back on startup.

## A reusable data helper

Instead of scattering `open()` calls everywhere, make one small helper file,
`data.py`, next to `main.py`:

```python
import json
import os

def load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
```

- `load(path, default)` reads the file, or returns a default (like `{}`) if it doesn't
  exist yet — so the bot doesn't crash on first run.
- `save(path, data)` writes the dictionary back. `indent=2` makes the file human-readable.

## Using it: a warnings system that persists

Make `cogs/warnings.py`:

```python
import discord
from discord import app_commands
from discord.ext import commands

import data

WARN_FILE = "warnings.json"


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = data.load(WARN_FILE, {})     # load saved warnings on startup

    @app_commands.command(description="Warn a member (saved).")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction, member: discord.Member, reason: str):
        key = str(member.id)                      # JSON keys must be strings
        self.warns.setdefault(key, [])
        self.warns[key].append(reason)
        data.save(WARN_FILE, self.warns)          # save after every change

        count = len(self.warns[key])
        await interaction.response.send_message(
            f"⚠️ Warned {member.mention}. They now have **{count}** warning(s).")

    @app_commands.command(description="See a member's warnings.")
    async def warnings(self, interaction, member: discord.Member):
        reasons = self.warns.get(str(member.id), [])
        if not reasons:
            await interaction.response.send_message(f"{member.mention} has no warnings.")
            return
        text = "\n".join(f"{i+1}. {r}" for i, r in enumerate(reasons))
        await interaction.response.send_message(f"**{member}'s warnings:**\n{text}")


async def setup(bot):
    await bot.add_cog(Warnings(bot))
```

The pattern to memorize:
1. **Load** the data in `__init__` (once, on startup).
2. **Change** it in memory (it's just a dictionary).
3. **Save** it after every change.

Two details worth noting:
- JSON keys are always **strings**, so we use `str(member.id)`.
- `setdefault(key, [])` gives a user an empty list the first time we warn them.

**▶ Test:** warn someone, restart the bot, then run `/warnings` on them — the warnings are
still there. 🎉

## When JSON is enough (and when it isn't)

JSON is great for hundreds or a few thousand records and simple data. If your bot gets huge
or needs to search/filter lots of data quickly, you'll want a real database — that's the
next lesson. For most community bots, JSON is honestly fine.

## Practice

**Challenge:** add a `/clearwarns` command (staff only) that empties a member's warnings and
saves.

<details><summary>Solution</summary>

```python
    @app_commands.command(description="Clear a member's warnings.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def clearwarns(self, interaction, member: discord.Member):
        self.warns[str(member.id)] = []
        data.save(WARN_FILE, self.warns)
        await interaction.response.send_message(f"Cleared {member.mention}'s warnings.")
```
</details>

## Recap

- Data in variables vanishes on restart; save it to a **JSON file** to persist.
- A tiny `data.py` with `load(path, default)` and `save(path, data)` keeps it clean.
- Pattern: **load on startup → change in memory → save after each change.**
- JSON keys are strings (`str(member.id)`).

→ **Next: Databases with SQLite**
