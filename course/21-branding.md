# A Branding System

Copying the same color and footer into every embed is tedious and easy to get wrong. The
pro move is to put all your branding in **one file** and reuse it everywhere. Change it
once, and the whole bot updates. This is how professional bots keep a consistent look.

## Step 1 — Make config.py

Create `config.py` next to `main.py`:

```python
import discord

# ---- Change this to rebrand the whole bot ----
STUDIO_NAME = "My Bot"
TAGLINE = "Made with discord.py"
BRAND_COLOR = discord.Color.from_str("#5865f2")
# ----------------------------------------------


def branded_embed(title=None, description=None):
    embed = discord.Embed(title=title, description=description, color=BRAND_COLOR)
    embed.set_footer(text=f"{STUDIO_NAME} • {TAGLINE}")
    return embed
```

`branded_embed()` is a helper (remember functions?) that hands back an embed already wearing
your color and footer.

## Step 2 — Use it in a cog

```python
from config import branded_embed, STUDIO_NAME

    @app_commands.command(description="Server info, branded.")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild
        embed = branded_embed(title=g.name, description=f"A {STUDIO_NAME} community.")
        embed.add_field(name="Members", value=g.member_count)
        await interaction.response.send_message(embed=embed)
```

Every embed you make this way matches automatically. Want a different color later? Change
the one line in `config.py`.

## Step 3 — Panels (the banner-on-top look)

Big, polished server panels often have a **banner image on top** and a **divider bar at the
bottom**. But a single embed can only hold *one* image. The trick: send **two embeds
together** — Discord stacks them into one seamless card.

Add this to `config.py`:

```python
BANNERS = {"welcome": None, "assistance": None}   # paste image links here later
DIVIDER_IMAGE = None                              # the thin bar at the bottom


def panel(title, description, banner=None):
    embeds = []
    if banner:
        top = discord.Embed(color=BRAND_COLOR)
        top.set_image(url=banner)
        embeds.append(top)

    body = discord.Embed(title=title, description=description, color=BRAND_COLOR)
    if DIVIDER_IMAGE:
        body.set_image(url=DIVIDER_IMAGE)
    body.set_footer(text=f"{STUDIO_NAME} • {TAGLINE}")
    embeds.append(body)
    return embeds
```

`panel()` returns a **list** of embeds. Send it like this:

```python
await interaction.channel.send(embeds=panel("Welcome!", "Thanks for joining."))
```

(Note the plural `embeds=` when sending a list.)

## Step 4 — Add the images

Upload your banner and divider images to a Discord channel, right-click → **Copy Link**, and
paste the links into `BANNERS` and `DIVIDER_IMAGE`. Now `panel()` produces the full
professional look — banner, title, text, divider bar — everywhere you use it.

## Practice

**Challenge:** add a `TAGLINE`-based `/about` command that posts a panel titled with your
studio name and a short description of what the studio does.

<details><summary>Solution</summary>

```python
from config import panel, STUDIO_NAME, TAGLINE, BANNERS

    @app_commands.command(description="About the studio.")
    async def about(self, interaction: discord.Interaction):
        embeds = panel(STUDIO_NAME, f"{TAGLINE}. We build custom designs and bots.",
                       banner=BANNERS.get("welcome"))
        await interaction.channel.send(embeds=embeds)
        await interaction.response.send_message("Posted!", ephemeral=True)
```
</details>

## Recap

- Keep branding in **`config.py`**: name, tagline, color, banners.
- `branded_embed()` reuses your style; `panel()` gives the banner-on-top look by sending
  **two embeds together**.
- Rebrand the whole bot by editing one file.

→ **Next: Buttons & Views**
