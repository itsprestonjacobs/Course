# Modals (Pop-up Forms)

A **modal** is a pop-up form — text boxes that appear over Discord when a user clicks a
button or runs a command. They're perfect for collecting longer input: a suggestion, a bug
report, the details of an order, or an application.

## The idea

A modal is a class that inherits `discord.ui.Modal`. You add `TextInput` fields to it. When
the user hits **Submit**, an `on_submit` callback runs with their answers.

## A suggestion box

```python
import discord
from discord import app_commands
from discord.ext import commands


class SuggestionModal(discord.ui.Modal, title="Submit a Suggestion"):
    idea = discord.ui.TextInput(
        label="Your suggestion",
        placeholder="What should we add?",
        style=discord.TextStyle.paragraph,   # multi-line box
        max_length=500,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Thanks! You suggested:\n> {self.idea.value}", ephemeral=True)


class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Open the suggestion form.")
    async def suggest(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SuggestionModal())


async def setup(bot):
    await bot.add_cog(Forms(bot))
```

- `discord.ui.Modal, title="…"` — the pop-up and its heading.
- `discord.ui.TextInput(...)` — each box. `self.idea.value` is what they typed.
- `send_modal(...)` opens it. Note: a command opens a modal *instead of* replying first.

**▶ Run `/suggest`** — a pop-up appears. Type something and submit.

## TextInput options

```python
name = discord.ui.TextInput(
    label="Name",
    style=discord.TextStyle.short,       # single line (default)
    placeholder="Type here…",
    required=True,
    max_length=100,
    default="",                          # pre-filled text
)
```

- `style=short` = one line; `style=paragraph` = a big multi-line box.
- Up to **5** text inputs per modal.

## Opening a modal from a button

Modals shine when combined with buttons — click a button, fill a form. This is how order and
application panels work:

```python
class OrderView(discord.ui.View):
    @discord.ui.button(label="Place Order", style=discord.ButtonStyle.green)
    async def order(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SuggestionModal())
```

## Sending the results somewhere useful

In `on_submit`, you can do anything with the answers — post them to a staff channel, save
them, open a ticket:

```python
    async def on_submit(self, interaction: discord.Interaction):
        log = discord.utils.get(interaction.guild.text_channels, name="suggestions")
        if log:
            embed = discord.Embed(description=self.idea.value, color=discord.Color.blurple())
            embed.set_author(name=str(interaction.user), icon_url=interaction.user.display_avatar.url)
            await log.send(embed=embed)
        await interaction.response.send_message("Suggestion submitted!", ephemeral=True)
```

## Practice

**Challenge:** make a `/report` command that opens a modal with two boxes — "Who" (short)
and "What happened" (paragraph) — and replies with a summary of both answers.

<details><summary>Solution</summary>

```python
class ReportModal(discord.ui.Modal, title="Report a Problem"):
    who = discord.ui.TextInput(label="Who")
    what = discord.ui.TextInput(label="What happened", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction):
        await interaction.response.send_message(
            f"**Report on {self.who.value}:**\n{self.what.value}", ephemeral=True)

    @app_commands.command(description="Report a problem.")
    async def report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ReportModal())
```
</details>

## Recap

- A **modal** is a pop-up form: `discord.ui.Modal` + `TextInput` fields.
- Open it with `interaction.response.send_modal(...)` (from a command or a button).
- Read answers in `on_submit` via `self.field.value`; up to 5 fields.

→ **Next: Persistent Components**
