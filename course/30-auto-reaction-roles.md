# Auto-roles & Reaction Roles

Let members give *themselves* roles — for pings, colors, or interests. We'll build a modern
**button role menu** (the clean way) and also cover classic **reaction roles**.

## Button roles (recommended)

You already know Views and persistence — button roles are just that applied to roles. Make
`cogs/roles.py`:

```python
import discord
from discord import app_commands
from discord.ext import commands

# (button label, emoji, role name) — edit this to match your server's roles
ROLE_BUTTONS = [
    ("Announcements", "📢", "Announcements"),
    ("Events", "🎉", "Events"),
    ("Updates", "🔔", "Updates"),
]


class RoleButton(discord.ui.Button):
    def __init__(self, label, emoji, role_name):
        super().__init__(label=label, emoji=emoji, style=discord.ButtonStyle.grey,
                         custom_id=f"role:{role_name}")
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name=self.role_name)
        if not role:
            await interaction.response.send_message("That role doesn't exist.", ephemeral=True)
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Removed **{role.name}**.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Gave you **{role.name}**.", ephemeral=True)


class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for label, emoji, role_name in ROLE_BUTTONS:
            self.add_item(RoleButton(label, emoji, role_name))


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(RoleView())        # persistent — survives restarts

    @app_commands.command(description="Post the self-roles menu (staff only).")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def rolemenu(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Pick your roles",
                              description="Click a button to toggle a role.",
                              color=discord.Color.blurple())
        await interaction.channel.send(embed=embed, view=RoleView())
        await interaction.response.send_message("Menu posted!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Roles(bot))
```

How it works:
- Each button is a `RoleButton` that remembers its role name.
- Clicking toggles the role: if you have it, it's removed; if not, it's added.
- The View is **persistent** (`timeout=None`, `custom_id`, `cog_load` + `add_view`) so the
  menu keeps working forever.

Create roles named `Announcements`, `Events`, `Updates` (and make sure the bot's role is
**above** them), then run `/rolemenu`. **▶ Click the buttons** to toggle roles.

## Classic reaction roles

Some servers still use emoji reactions on a message. The bot listens for reactions and adds
the matching role. Because a reaction can happen on any old message, we use the **raw**
event `on_raw_reaction_add`:

```python
    # map an emoji to a role name
    REACTION_ROLES = {"📢": "Announcements", "🎉": "Events"}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        role_name = self.REACTION_ROLES.get(str(payload.emoji))
        if not role_name:
            return
        guild = self.bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=role_name)
        member = guild.get_member(payload.user_id)
        if role and member and not member.bot:
            await member.add_roles(role)
```

Button roles are generally nicer (no leftover reactions, cleaner UI), but now you know both.

## Practice

**Challenge:** add a fourth entry to `ROLE_BUTTONS` for a "Giveaways" role with the 🎁 emoji,
create the role in your server, and confirm the button toggles it.

## Recap

- **Button roles**: a persistent View of `RoleButton`s that toggle a role on click — the
  modern approach.
- **Reaction roles**: listen to `on_raw_reaction_add` and map emoji → role.
- Both need **Manage Roles** and the bot's role **above** the roles it hands out.

→ **Next: Auto-moderation**
