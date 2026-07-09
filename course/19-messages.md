# Sending Messages & DMs

Before embeds and buttons, let's master plain messages — sending, replying, editing,
deleting, and DMing. These are the building blocks everything else sits on.

## Sending to a channel

Any channel object has a `.send()`:

```python
    @app_commands.command(description="Announce something.")
    async def announce(self, interaction: discord.Interaction, text: str):
        await interaction.channel.send(text)
        await interaction.response.send_message("Sent!", ephemeral=True)
```

`interaction.channel` is where the command was used. You can also send to a *specific*
channel you look up.

## Mentions and formatting

Discord uses simple markdown, plus special mention objects:

```python
await channel.send(f"Hello {interaction.user.mention}!")   # pings the user
await channel.send("**bold**, *italic*, `code`, ~~strike~~")
await channel.send("Line one\nLine two")                   # \n = new line
```

- `member.mention` → a clickable @user
- `role.mention` → a clickable @role
- `channel.mention` → a clickable #channel

## Replying vs. sending

A **reply** visually links your message to another:

```python
@commands.Cog.listener()
async def on_message(self, message):
    if message.author.bot:
        return
    if message.content == "ping":
        await message.reply("pong!")     # shows as a reply to their message
```

## Editing and deleting

`send()` and `reply()` hand back the message they created, so you can change it later:

```python
msg = await channel.send("Loading…")
await msg.edit(content="Done! ✅")
await msg.delete()
```

## Direct messages (DMs)

To DM a member, call `.send()` on the *member* instead of a channel:

```python
    @app_commands.command(description="DM a member.")
    async def dm(self, interaction: discord.Interaction, member: discord.Member, text: str):
        try:
            await member.send(text)
            await interaction.response.send_message("Sent them a DM!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("They have DMs closed.", ephemeral=True)
```

> ⚠️ DMs fail if the member has them disabled — Discord raises `discord.Forbidden`. Always
> wrap DM sends in `try / except` so the command doesn't crash. (Remember `try/except` from
> the Python lessons? This is where it earns its keep.)

## Sending files

```python
await channel.send(file=discord.File("image.png"))
```

We'll use this for ticket transcripts (sending a `.txt` file).

## Practice

Make an `/echo` command that replies with what you typed, then edits it after "thinking":

```python
    @app_commands.command(description="Echo with a twist.")
    async def echo(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message("🤔 thinking…")
        msg = await interaction.original_response()
        await msg.edit(content=text)
```

**Challenge:** make a `/dmme` command that sends *you* (the person running it) a DM saying
"Here's your DM!". (Hint: `interaction.user` is a member — you can `.send()` to it.)

<details><summary>Solution</summary>

```python
    @app_commands.command(description="DM yourself.")
    async def dmme(self, interaction: discord.Interaction):
        try:
            await interaction.user.send("Here's your DM!")
            await interaction.response.send_message("Check your DMs!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Your DMs are closed.", ephemeral=True)
```
</details>

## Recap

- `channel.send(text)` sends; `message.reply(text)` links to a message.
- `.mention` makes clickable pings; `\n`, `**bold**`, `` `code` `` format text.
- `send()` returns the message → `.edit()` / `.delete()` it later.
- DM with `member.send(...)`, always wrapped in `try / except discord.Forbidden`.

→ **Next: Embeds Deep Dive**
