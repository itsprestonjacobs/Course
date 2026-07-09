import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Check if the bot is alive.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! 🏓 ({latency}ms)")

    @app_commands.command(description="Show all commands.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Commands", color=discord.Color.blurple())
        for cmd in sorted(self.bot.tree.get_commands(), key=lambda c: c.name):
            embed.add_field(name=f"/{cmd.name}", value=cmd.description or "…", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(General(bot))
