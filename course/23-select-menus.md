# Select Menus (Dropdowns)

A **select menu** is a dropdown — like the "Pick a category" menus on support panels. It's
perfect when you have several options and buttons would be too many. This is the component
our ticket system uses.

## The idea

A select menu is a component (like a button) that you add to a View. Each option is a
`SelectOption`. When someone picks one, a callback runs with their choice.

## A basic dropdown

```python
import discord
from discord import app_commands
from discord.ext import commands


class FlavorSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Chocolate", description="Rich and dark", emoji="🍫"),
            discord.SelectOption(label="Vanilla", description="Classic", emoji="🍦"),
            discord.SelectOption(label="Strawberry", description="Fruity", emoji="🍓"),
        ]
        super().__init__(placeholder="Pick a flavor…", options=options)

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]        # what they picked
        await interaction.response.send_message(f"You picked **{choice}**!", ephemeral=True)


class FlavorView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(FlavorSelect())


class Menus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Pick a flavor.")
    async def flavor(self, interaction: discord.Interaction):
        await interaction.response.send_message("Choose:", view=FlavorView())


async def setup(bot):
    await bot.add_cog(Menus(bot))
```

Key points:
- A dropdown is a class that inherits `discord.ui.Select`.
- `options` is a list of `SelectOption`s (label, description, emoji).
- `placeholder` is the greyed-out text before a choice is made.
- In the callback, `self.values[0]` is what the user selected.
- We add the select to a View with `self.add_item(...)`.

**▶ Run it** and try `/flavor`.

## Building options from a list

Hard-coding options is fine, but building them from a list is cleaner — change the list,
change the menu:

```python
CATEGORIES = [
    ("General Support", "Questions or feedback", "💬"),
    ("Payment / Refund", "Billing help", "💳"),
    ("Partnership", "Work together", "🤝"),
]

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=label, description=desc, emoji=emoji)
            for label, desc, emoji in CATEGORIES
        ]
        super().__init__(placeholder="What do you need help with?", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Opening a **{self.values[0]}** ticket…", ephemeral=True)
```

This is almost exactly the ticket panel you'll build in the projects module — you're
already most of the way there.

## Allowing multiple picks

By default users pick one. Allow a range with `min_values` / `max_values`:

```python
super().__init__(placeholder="Pick up to 3", options=options, min_values=1, max_values=3)
```

Then `self.values` is a list of *all* their picks.

## Practice

**Challenge:** make a `/color` command with a dropdown of three colors. When picked, reply
with an embed whose color matches the choice. (Hint: keep a dict mapping the label to a
`discord.Color`.)

<details><summary>Solution</summary>

```python
COLORS = {"Red": discord.Color.red(), "Green": discord.Color.green(), "Blue": discord.Color.blue()}

class ColorSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=name) for name in COLORS]
        super().__init__(placeholder="Pick a color", options=options)

    async def callback(self, interaction):
        name = self.values[0]
        embed = discord.Embed(title=name, color=COLORS[name])
        await interaction.response.send_message(embed=embed, ephemeral=True)
```
</details>

## Recap

- A dropdown inherits `discord.ui.Select`; options are `SelectOption`s.
- The callback reads `self.values[0]` (or the whole list if multi-select).
- Add it to a View with `add_item()`.
- Build options from a list to keep them easy to edit — the ticket panel pattern.

→ **Next: Modals (Pop-up Forms)**
