# Embeds Deep Dive

Embeds are the clean, colored cards that make a bot look professional — like the support and
info panels you see in well-run Discord servers. This lesson covers every part.

## Your first embed

```python
    @app_commands.command(description="Show an example embed.")
    async def demo(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Hello!",
            description="This is the body of the embed.",
            color=discord.Color.from_str("#1e9bff"),
        )
        await interaction.response.send_message(embed=embed)
```

Notice we send `embed=embed` instead of a plain string.

## The anatomy

An embed has a lot of parts. Here they all are:

```python
embed = discord.Embed(
    title="Order Status",
    description="Everything you can put in the body goes here.",
    color=discord.Color.from_str("#1e9bff"),
)

embed.set_author(name="My Bot", icon_url="https://.../logo.png")
embed.set_thumbnail(url="https://.../small.png")     # small image, top-right
embed.add_field(name="Discord Services", value="🟢 Open", inline=True)
embed.add_field(name="Custom Embeds", value="🟢 Open", inline=True)
embed.add_field(name="Note", value="Open a ticket to order.", inline=False)
embed.set_image(url="https://.../banner.png")        # big image, bottom
embed.set_footer(text="Made with discord.py")
```

| Method | What it does |
|--------|--------------|
| `title` / `description` | headline and body text |
| `color` | the stripe down the left edge |
| `add_field(name, value, inline)` | a labeled mini-section; `inline=True` puts them side by side |
| `set_thumbnail(url)` | small image in the top-right |
| `set_image(url)` | large image at the bottom |
| `set_author(name, icon_url)` | small name+icon at the very top |
| `set_footer(text)` | small text at the bottom |

## Colors

```python
color=discord.Color.from_str("#1e9bff")   # any hex code
color=discord.Color.red()                 # built-in colors
color=discord.Color.green()
color=discord.Color.gold()
```

Use one brand color for your normal embeds, and red/green for errors/success — a visual
language your users learn instantly.

## Fields and inline layout

Fields are the key to nice layouts. `inline=True` fields flow left-to-right (up to 3 per
row); `inline=False` fields take a full row. That's how a tidy "status" or "stats" panel
lines up so neatly.

## Getting image links

Embeds need image **URLs**, not files on your computer. The easy way: upload the image to
any Discord channel, right-click it → **Copy Link**, and paste that URL.

## A real example: /serverinfo

```python
    @app_commands.command(description="Show info about this server.")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild
        embed = discord.Embed(title=g.name, color=discord.Color.from_str("#1e9bff"))
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        embed.add_field(name="Members", value=g.member_count, inline=True)
        embed.add_field(name="Channels", value=len(g.channels), inline=True)
        embed.add_field(name="Created", value=g.created_at.strftime("%b %d, %Y"), inline=True)
        embed.set_footer(text="My Bot")
        await interaction.response.send_message(embed=embed)
```

## Practice

**Challenge:** build a `/profile` command that shows an embed with the user's name as the
title, their avatar as the thumbnail (`interaction.user.display_avatar.url`), and a field
for when they joined Discord (`interaction.user.created_at`).

<details><summary>Solution</summary>

```python
    @app_commands.command(description="Show your profile.")
    async def profile(self, interaction: discord.Interaction):
        u = interaction.user
        embed = discord.Embed(title=u.display_name, color=discord.Color.from_str("#1e9bff"))
        embed.set_thumbnail(url=u.display_avatar.url)
        embed.add_field(name="Joined Discord", value=u.created_at.strftime("%b %d, %Y"))
        await interaction.response.send_message(embed=embed)
```
</details>

## Recap

- Build with `discord.Embed(title=, description=, color=)` and send `embed=embed`.
- Add `add_field`, `set_thumbnail`, `set_image`, `set_author`, `set_footer`.
- `inline=True` fields sit side by side — the secret to clean panels.
- Images need **URLs** (upload → Copy Link).

→ **Next: A Branding System**
