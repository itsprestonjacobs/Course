import discord
from discord import app_commands
from discord.ext import commands

import data

WARN_FILE = "warnings.json"


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = data.load(WARN_FILE, {})

    @app_commands.command(description="Warn a member (saved).")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        key = str(member.id)
        self.warns.setdefault(key, [])
        self.warns[key].append(reason)
        data.save(WARN_FILE, self.warns)

        count = len(self.warns[key])
        await interaction.response.send_message(
            f"⚠️ Warned {member.mention}. They now have **{count}** warning(s).")
        try:
            await member.send(f"You were warned in **{interaction.guild.name}**: {reason}")
        except discord.Forbidden:
            pass

    @app_commands.command(description="See a member's warnings.")
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        reasons = self.warns.get(str(member.id), [])
        if not reasons:
            await interaction.response.send_message(f"{member.mention} has no warnings.")
            return
        text = "\n".join(f"{i + 1}. {r}" for i, r in enumerate(reasons))
        await interaction.response.send_message(f"**{member}'s warnings:**\n{text}")

    @app_commands.command(description="Clear a member's warnings.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def clearwarns(self, interaction: discord.Interaction, member: discord.Member):
        self.warns[str(member.id)] = []
        data.save(WARN_FILE, self.warns)
        await interaction.response.send_message(f"Cleared {member.mention}'s warnings.")


async def setup(bot):
    await bot.add_cog(Warnings(bot))
