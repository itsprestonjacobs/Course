# Calling Web APIs & Webhooks

Your bot can reach out to the wider internet — fetch a meme, the weather, a random fact, or
crypto prices — by calling **web APIs**. And other services can push messages *into* your
server through **webhooks**. Both make your bot feel connected to the world.

## Calling an API with aiohttp

Because a bot is async, we use the async HTTP library **aiohttp** (it comes with
discord.py). Install nothing extra — just import it.

```python
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands


class Web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Get a random dad joke.")
    async def joke(self, interaction: discord.Interaction):
        await interaction.response.defer()          # calls take a moment
        url = "https://icanhazdadjoke.com/"
        headers = {"Accept": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                data = await resp.json()

        await interaction.followup.send(f"😂 {data['joke']}")


async def setup(bot):
    await bot.add_cog(Web(bot))
```

The shape to remember:
- `defer()` first — network calls can be slow (the 3-second rule again).
- `async with aiohttp.ClientSession()` opens a session.
- `await resp.json()` reads the response as a dictionary — then you pull out the fields you
  want (`data['joke']`).

## Handling failures

The internet is unreliable. Wrap API calls so a hiccup doesn't crash the command:

```python
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await interaction.followup.send("The service is down right now.")
                        return
                    data = await resp.json()
        except aiohttp.ClientError:
            await interaction.followup.send("Couldn't reach the service.")
            return
```

`resp.status` is the HTTP code — `200` means OK.

## Reading JSON responses

Most APIs return JSON, which becomes a Python dictionary (remember dictionaries and
`.get()`?). If the structure is nested, you dig in with keys and indexes:

```python
data = await resp.json()
temp = data["main"]["temp"]           # nested dict
first = data["results"][0]["name"]    # a list inside a dict
```

## Incoming webhooks

A **webhook** is a special URL that posts a message to a channel — no bot code needed on the
sending side. Useful for alerts from GitHub, uptime monitors, or your own website.

Create one in Discord: **Channel Settings → Integrations → Webhooks → New Webhook**, then
copy its URL. Anything can `POST` JSON to that URL to make a message appear. From Python:

```python
        webhook_url = "https://discord.com/api/webhooks/…"
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            await webhook.send("Alert: something happened!", username="Monitor")
```

> 🔒 Treat a webhook URL like a password — anyone with it can post to your channel. Keep it
> in your `.env`, not in your code.

## Practice

**Challenge:** make a `/cat` command that fetches a random cat image from
`https://api.thecatapi.com/v1/images/search` (returns a list; the URL is
`data[0]["url"]`) and sends it in an embed with `embed.set_image(url=...)`.

<details><summary>Solution</summary>

```python
    @app_commands.command(description="Random cat.")
    async def cat(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as resp:
                data = await resp.json()
        embed = discord.Embed(title="🐱 Meow")
        embed.set_image(url=data[0]["url"])
        await interaction.followup.send(embed=embed)
```
</details>

## Recap

- Call web APIs with **aiohttp**: `defer()` → `ClientSession` → `session.get(url)` →
  `resp.json()`.
- Check `resp.status` and wrap calls in `try/except` for reliability.
- **Webhooks** are URLs that post into a channel; keep their URLs secret.

→ **Next: Git & GitHub for Your Bot**
