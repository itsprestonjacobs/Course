import discord
from discord import app_commands
from discord.ext import commands

from config import ROLE_BUTTONS   # edit the list in config.py to change these


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
        self.bot.add_view(RoleView())

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
