# Welcome & Leave Messages

A friendly welcome makes a server feel alive. This is our first feature built entirely on
**events** rather than commands — the bot reacts automatically when someone joins or leaves.

## Step 1 — The cog

Make `cogs/welcome.py`:

```python
import discord
from discord.ext import commands

WELCOME_CHANNEL = "welcome"     # the channel name to post in

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Welcome(bot))
```

Add `"cogs.welcome"` to `COGS`, and create a channel called `welcome` in your server.

## Step 2 — Greet new members

Inside the class, add a listener (remember: events in cogs use `@commands.Cog.listener()`):

```python
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL)
        if not channel:
            return

        embed = discord.Embed(
            title=f"Welcome, {member.name}! 👋",
            description=f"Hey {member.mention}, welcome to **{member.guild.name}**!\n"
                        "Grab your roles and say hi.",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"You're member #{member.guild.member_count}")
        await channel.send(embed=embed)
```

- `discord.utils.get(...)` finds a channel by name — a super common helper.
- `member.guild.member_count` lets us show "member #42".

**▶ Test it** — you can't easily rejoin, so test by having a friend join, or use a second
account.

## Step 3 — Goodbye messages

```python
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL)
        if channel:
            await channel.send(f"**{member.name}** has left the server. 👋")
```

## Step 4 — Auto-assign a starter role (bonus)

Give every new member a default role automatically:

```python
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="Member")
        if role:
            await member.add_roles(role)
```

> ⚠️ For this the bot needs **Manage Roles**, and its role must sit **above** the "Member"
> role (hierarchy again!). We build a fuller auto-role + reaction-role system next lesson.

## Making the channel configurable

Right now the channel name is hardcoded as `"welcome"`. That's fine for one server, but in
the **Data & Storage** module you'll learn to store this per-server so admins can pick their
own channel with a command. For now, hardcoding is perfectly okay.

## Practice

**Challenge:** make the goodbye message an embed (red color) with the member's avatar as the
thumbnail, matching the style of the welcome embed.

<details><summary>Solution</summary>

```python
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL)
        if not channel:
            return
        embed = discord.Embed(title=f"Goodbye, {member.name}",
                              description="We'll miss you!", color=discord.Color.red())
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)
```
</details>

## Recap

- Welcome/leave are **event-driven**: `on_member_join` / `on_member_remove` listeners in a cog.
- `discord.utils.get(guild.text_channels, name=...)` finds a channel by name.
- `member.add_roles(role)` can auto-assign a starter role (needs Manage Roles + hierarchy).

→ **Next: Auto-roles & Reaction Roles**
