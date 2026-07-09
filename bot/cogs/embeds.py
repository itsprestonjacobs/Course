import discord
from discord import app_commands
from discord.ext import commands

from config import BRAND_COLOR, STUDIO_NAME, TAGLINE, BANNERS, branded_embed, panel


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Show info about this server.")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild

        embed = branded_embed(title=g.name, description=g.description or f"A {STUDIO_NAME} community.")
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)

        embed.add_field(name="Members", value=g.member_count, inline=True)
        embed.add_field(name="Channels", value=len(g.channels), inline=True)
        embed.add_field(name="Roles", value=len(g.roles), inline=True)
        embed.add_field(name="Owner", value=g.owner.mention if g.owner else "Unknown", inline=True)
        embed.add_field(name="Created", value=g.created_at.strftime("%b %d, %Y"), inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Post a branded announcement panel.")
    @app_commands.describe(title="Panel title", message="What it should say")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def announce(self, interaction: discord.Interaction, title: str, message: str):
        await interaction.channel.send(embeds=panel(title, message, banner=BANNERS["welcome"]))
        await interaction.response.send_message("Posted!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Embeds(bot))
