# Embed Recipes & Custom Embeds

You know the parts of an embed — now here's a cookbook of **ready-to-use custom embeds**,
plus a `/embed` command that lets staff build embeds *live* without touching code. Copy any
recipe and tweak it.

## A custom embed builder (no code needed)

The slickest way to let your team make custom embeds is a **modal** (remember modals?).
This `/embed` command pops up a form — title, description, color, image — and posts the
result. Add it to your `Embeds` cog:

```python
from config import BRAND_COLOR, STUDIO_NAME

class EmbedBuilder(discord.ui.Modal, title="Create a Custom Embed"):
    e_title = discord.ui.TextInput(label="Title", required=False, max_length=256)
    e_desc = discord.ui.TextInput(label="Description", style=discord.TextStyle.paragraph,
                                  required=False, max_length=2000)
    e_color = discord.ui.TextInput(label="Color hex (e.g. #1e9bff)", required=False, max_length=7)
    e_image = discord.ui.TextInput(label="Image URL (optional)", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            color = discord.Color.from_str(self.e_color.value) if self.e_color.value else BRAND_COLOR
        except ValueError:
            color = BRAND_COLOR
        embed = discord.Embed(title=self.e_title.value or None,
                              description=self.e_desc.value or None, color=color)
        if self.e_image.value:
            embed.set_image(url=self.e_image.value)
        embed.set_footer(text=STUDIO_NAME)
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Embed posted!", ephemeral=True)

    @app_commands.command(description="Build and post a custom embed (staff only).")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def embed(self, interaction: discord.Interaction):
        await interaction.response.send_modal(EmbedBuilder())
```

**▶ Run `/embed`** — fill in the form, hit submit, and your custom embed appears. Now
non-coders on your team can make branded embeds any time.

## Recipe: rules

```python
embed = discord.Embed(title="📜 Server Rules", color=discord.Color.from_str("#1e9bff"))
embed.description = (
    "**1.** Be respectful to everyone.\n"
    "**2.** No spam or self-promotion.\n"
    "**3.** Keep content safe for work.\n"
    "**4.** Listen to staff.\n"
    "**5.** Have fun!"
)
embed.set_footer(text="Breaking the rules may result in a warning, mute, or ban.")
```

## Recipe: an "Order Status" panel

A service-status panel — colored dots make each item pop:

```python
services = {
    "Discord Services": "🟢 Open",
    "Custom Embeds": "🟢 Open",
    "Graphics": "🟢 Open",
    "Liveries": "🟡 Delayed",
    "Uniforms": "🔴 Closed",
}
lines = "\n".join(f"**{name}:** {status}" for name, status in services.items())
embed = discord.Embed(title="🛒 Order Status", description=lines,
                      color=discord.Color.from_str("#1e9bff"))
embed.set_footer(text="Open a ticket to place an order!")
```

Build the list from a **dictionary** so updating a status is a one-line change.

## Recipe: a giveaway

```python
embed = discord.Embed(title="🎉 GIVEAWAY 🎉", color=discord.Color.gold())
embed.description = "**Prize:** Custom logo design\nReact with 🎉 to enter!"
embed.add_field(name="Hosted by", value=interaction.user.mention)
embed.add_field(name="Ends", value="in 24 hours")
```

## Recipe: a poll

```python
embed = discord.Embed(title="📊 Poll", description="Should we host a movie night?",
                      color=discord.Color.blurple())
msg = await interaction.channel.send(embed=embed)
await msg.add_reaction("👍")
await msg.add_reaction("👎")
```

## Recipe: a profile / rank card

```python
u = interaction.user
embed = discord.Embed(title=f"{u.display_name}'s Profile", color=u.color)
embed.set_thumbnail(url=u.display_avatar.url)
embed.add_field(name="Joined", value=u.joined_at.strftime("%b %d, %Y"))
embed.add_field(name="Top role", value=u.top_role.mention)
```

## Recipe: success & error embeds

Give your bot a consistent visual language — green for good, red for bad:

```python
def success(text):
    return discord.Embed(description=f"✅ {text}", color=discord.Color.green())

def error(text):
    return discord.Embed(description=f"❌ {text}", color=discord.Color.red())

# usage:
await interaction.response.send_message(embed=success("Settings saved!"))
```

## Adding fields in a loop

For lists that change, build fields programmatically:

```python
embed = discord.Embed(title="🏆 Top Members", color=discord.Color.gold())
for i, (name, score) in enumerate(top_members, start=1):
    embed.add_field(name=f"#{i} — {name}", value=f"{score} points", inline=False)
```

## Practice

**Challenge:** make a `/announce`-style command that opens the `EmbedBuilder` modal but also
pings `@everyone` when it posts. (Hint: send `content="@everyone"` alongside the embed, and
allow the mention with `allowed_mentions=discord.AllowedMentions(everyone=True)`.)

## Recap

- `/embed` + a **modal** lets your team build custom embeds with no code.
- Keep a cookbook: rules, status panels, giveaways, polls, profiles, success/error embeds.
- Build repetitive embeds (status lists, leaderboards) from **dictionaries/loops**.

→ **Next: A Branding System**
