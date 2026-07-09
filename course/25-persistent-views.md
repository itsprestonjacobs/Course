# Persistent Components

There's a catch with everything you built in the last three lessons: **when the bot
restarts, the buttons and dropdowns stop working.** For a ticket panel that sits in a
channel forever, that's a dealbreaker. This lesson fixes it — and it's short but important.

## Why buttons "die" on restart

When your bot starts, it forgets about every View it made before. So an old panel's button
click arrives, and the bot goes "I don't know what that button is" — nothing happens.

The fix has two parts: give components a permanent **`custom_id`**, and **re-register** the
View when the bot starts.

## Part 1 — timeout=None and custom_id

A normal View times out after a few minutes. A persistent one must set `timeout=None`, and
every component needs a fixed `custom_id`:

```python
class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)          # never expires

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.blurple,
                       custom_id="ticket:open")  # permanent name
    async def open(self, interaction, button):
        await interaction.response.send_message("Opening a ticket…", ephemeral=True)
```

The `custom_id` is how Discord tells the restarted bot *which* button was clicked. It must
be unique and stable (don't change it later).

## Part 2 — re-register on startup

In the cog, add a `cog_load` method that registers the View when the bot boots:

```python
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(TicketPanel())    # reconnect the buttons after a restart
```

`add_view` tells the bot "if you see a component with these custom_ids, run this View's
code." Now old panels work forever.

## Selects and modals too

Dropdowns follow the same rule — give the `Select` a `custom_id` and put it in a
`timeout=None` View that you `add_view` on startup:

```python
class TicketDropdown(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Pick…", options=[...], custom_id="ticket:pick")
```

Modals don't need this — they're opened fresh each time by a button or command, so there's
nothing to persist.

## The rule of thumb

> If a message with components is meant to **live in a channel long-term** (a ticket panel,
> a role menu), make its View persistent: `timeout=None` + `custom_id` on every component +
> `add_view` in `cog_load`.
>
> If it's a **throwaway** prompt (a confirm dialog you send and forget), you don't need any
> of this — a normal View is fine.

## Practice

**Challenge:** take the `HelloView` button from the Buttons lesson and make it persistent —
add `timeout=None`, a `custom_id`, and register it in `cog_load`.

<details><summary>Solution</summary>

```python
class HelloView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Click me!", custom_id="hello:click")
    async def hi(self, interaction, button):
        await interaction.response.send_message("Clicked!", ephemeral=True)

# in the cog:
    async def cog_load(self):
        self.bot.add_view(HelloView())
```
</details>

## Recap

- Buttons/dropdowns stop working after a restart unless they're **persistent**.
- Persistent = `timeout=None` + a stable **`custom_id`** on every component + `add_view()` in
  `cog_load`.
- Throwaway prompts don't need this; long-lived panels do.

→ **Next: Permissions & Role Hierarchy**
