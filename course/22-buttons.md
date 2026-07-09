# Buttons & Views

Buttons turn your bot from "type a command" into "click a thing." They're the foundation of
ticket panels, confirmation prompts, and role menus. The container that holds buttons is
called a **View**.

## The idea

- A **View** is a box of interactive components (buttons, dropdowns).
- You attach a View to a message when you send it.
- When someone clicks a button, discord.py runs the matching function (its **callback**).

## Your first button

```python
import discord
from discord import app_commands
from discord.ext import commands


class HelloView(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.blurple, emoji="👋")
    async def say_hi(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked it!", ephemeral=True)


class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Send a button.")
    async def button(self, interaction: discord.Interaction):
        await interaction.response.send_message("Here's a button:", view=HelloView())


async def setup(bot):
    await bot.add_cog(Buttons(bot))
```

- `class HelloView(discord.ui.View)` — a View (remember inheritance? we're building on
  discord.py's View).
- `@discord.ui.button(...)` turns the method below it into a clickable button.
- The callback gets its own `interaction` for *that click*.
- We attach it with `view=HelloView()` when sending.

**▶ Run it** and click the button — it replies just to you.

## Button styles

```python
discord.ButtonStyle.blurple    # primary / blue
discord.ButtonStyle.grey       # secondary
discord.ButtonStyle.green      # success
discord.ButtonStyle.red        # danger
discord.ButtonStyle.link       # a link button (needs url=, no callback)
```

```python
@discord.ui.button(label="Delete", style=discord.ButtonStyle.red, emoji="🗑️")
```

## Multiple buttons = a confirmation prompt

Add more `@discord.ui.button` methods and you get more buttons. A classic Yes/No:

```python
class Confirm(discord.ui.View):
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction, button):
        await interaction.response.edit_message(content="Confirmed! ✅", view=None)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction, button):
        await interaction.response.edit_message(content="Cancelled.", view=None)
```

`edit_message(..., view=None)` updates the original message and removes the buttons so they
can't be clicked twice.

## Link buttons

Link buttons open a URL — no callback needed:

```python
class Links(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Our Website", url="https://example.com"))
```

The Pricing / ToS buttons on the Derpy's Designs panels are exactly this.

## Practice

**Challenge:** make a `/vote` command with two buttons, 👍 and 👎, that each reply
"Thanks for voting!" (ephemeral).

<details><summary>Solution</summary>

```python
class Vote(discord.ui.View):
    @discord.ui.button(emoji="👍", style=discord.ButtonStyle.green)
    async def up(self, interaction, button):
        await interaction.response.send_message("Thanks for voting!", ephemeral=True)

    @discord.ui.button(emoji="👎", style=discord.ButtonStyle.red)
    async def down(self, interaction, button):
        await interaction.response.send_message("Thanks for voting!", ephemeral=True)
```
</details>

## Recap

- A **View** holds components; attach it with `view=...` when sending.
- `@discord.ui.button(...)` makes a button; its method is the click **callback**.
- Styles: blurple, grey, green, red, link. Use `edit_message(view=None)` to disable after a
  click.
- **Link buttons** open URLs with no callback.

→ **Next: Select Menus (Dropdowns)**
