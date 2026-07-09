import discord
from discord import app_commands
from discord.ext import commands

import settings


class BotSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Set the welcome/leave channel.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_welcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        settings.set_value(interaction.guild.id, "welcome_channel", channel.name)
        await interaction.response.send_message(
            f"Welcome messages will now go to {channel.mention}.", ephemeral=True)

    @app_commands.command(description="Set the mod-log channel.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_logs(self, interaction: discord.Interaction, channel: discord.TextChannel):
        settings.set_value(interaction.guild.id, "log_channel", channel.name)
        await interaction.response.send_message(
            f"Logs will now go to {channel.mention}.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(BotSettings(bot))
