import discord

# ============================================================
#  BRANDING — change this stuff to make the bot your own.
#  Everything below is used across every panel and embed, so
#  editing it here rebrands the whole bot in one place.
# ============================================================

STUDIO_NAME = "Derpy's Designs"
TAGLINE = "Where Creativity Meets Precision"

# The color of the stripe down the side of every embed.
BRAND_COLOR = discord.Color.from_str("#1e9bff")

# Banner images that sit on TOP of a panel.
# To get a link: upload the image to any Discord channel, then right-click it
# -> Copy Link, and paste it here. Leave as None to show no banner.
BANNERS = {
    "assistance": None,   # the "Assistance" header image
    "market": None,       # the "Market" header image
    "welcome": None,
}

# The thin bar shown at the BOTTOM of a panel (the blue "D" strip).
# Same trick: upload it, copy link, paste here. None = no bar.
DIVIDER_IMAGE = None


def branded_embed(title=None, description=None):
    """A normal embed already wearing our colors and footer."""
    embed = discord.Embed(title=title, description=description, color=BRAND_COLOR)
    embed.set_footer(text=f"{STUDIO_NAME} • {TAGLINE}")
    return embed


def panel(title, description, banner=None):
    """Build a 'panel' — the polished, banner-on-top look from the Derpy's
    Designs server. Returns a LIST of embeds you send together with
    `channel.send(embeds=panel(...))`.

    Trick: Discord stacks several embeds in one message into a single card.
    So we put the banner image in its own embed on top, then the real content
    below it, and finish with the divider bar.
    """
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
