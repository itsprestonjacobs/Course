# Error Handling & a Help Command

Two things that separate a hobby bot from a polished one: it never crashes on a user's
mistake, and it can explain itself. Let's add global error handling and a clean help
command.

## A global error handler

You've added per-cog handlers. For anything they don't catch, set up one **global** handler
in `main.py` so no error ever goes unhandled:

```python
@bot.tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        msg = "You don't have permission to use that."
    elif isinstance(error, app_commands.CommandOnCooldown):
        msg = f"⏳ Try again in {error.retry_after:.0f}s."
    else:
        msg = "Something went wrong. Please try again."
        print(f"Unhandled error: {error}")     # log the real error for yourself

    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)
```

The user sees a friendly message; you get the real error printed in your terminal to debug.

## Logging instead of print()

`print()` is fine while learning, but Python's `logging` module is better for a running bot
— it timestamps everything and can write to a file:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
log = logging.getLogger("bot")

log.info("Bot starting up")
log.warning("Something looks off")
log.error("An error happened")
```

Now you have a `bot.log` file recording what happened, even while you're away.

## A help command

Auto-build a help embed by asking the command tree what commands exist:

```python
    @app_commands.command(description="Show all commands.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Commands", color=discord.Color.blurple())
        for cmd in sorted(self.bot.tree.get_commands(), key=lambda c: c.name):
            embed.add_field(name=f"/{cmd.name}", value=cmd.description or "…", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
```

`self.bot.tree.get_commands()` returns every slash command, so this help stays up to date
automatically as you add commands. **▶ Try `/help`.**

## Grouping commands (bonus)

For a lot of commands, **groups** keep them tidy — `/ticket open`, `/ticket close`:

```python
    ticket = app_commands.Group(name="ticket", description="Ticket commands")

    @ticket.command(name="open", description="Open a ticket")
    async def open(self, interaction: discord.Interaction):
        ...

    @ticket.command(name="close", description="Close a ticket")
    async def close(self, interaction: discord.Interaction):
        ...
```

Discord shows them nested under `/ticket`, which is much cleaner for big bots.

## Practice

**Challenge:** extend the global error handler to catch `app_commands.CommandNotFound` and
silently ignore it (it happens when a command was removed but Discord still shows it briefly).

<details><summary>Solution</summary>

```python
    if isinstance(error, app_commands.CommandNotFound):
        return
```
(Add it as the first check in the handler.)
</details>

## Recap

- Add a **global** `@bot.tree.error` handler so no error is unhandled; show users a friendly
  message and log the real one.
- Use the **`logging`** module (with a file handler) instead of `print` for a real bot.
- A `/help` command built from `bot.tree.get_commands()` stays current automatically.
- **Command groups** (`app_commands.Group`) nest related commands.

→ **Next: Calling Web APIs & Webhooks**
