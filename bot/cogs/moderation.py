import datetime

import discord
from discord import app_commands
from discord.ext import commands

RED = discord.Color.red()
GREEN = discord.Color.green()


def result_embed(action, member, moderator, reason, color):
    embed = discord.Embed(color=color, timestamp=datetime.datetime.now())
    embed.title = action
    embed.add_field(name="Member", value=f"{member} ({member.id})", inline=False)
    embed.add_field(name="Moderator", value=moderator.mention, inline=False)
    embed.add_field(name="Reason", value=reason or "No reason given", inline=False)
    return embed


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Kick a member from the server.")
    @app_commands.describe(member="Who to kick", reason="Why")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "You can't kick someone with a role equal to or higher than yours.",
                ephemeral=True,
            )
            return

        await member.kick(reason=reason)
        embed = result_embed("Member Kicked", member, interaction.user, reason, RED)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Ban a member from the server.")
    @app_commands.describe(member="Who to ban", reason="Why")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "You can't ban someone with a role equal to or higher than yours.",
                ephemeral=True,
            )
            return

        await member.ban(reason=reason)
        embed = result_embed("Member Banned", member, interaction.user, reason, RED)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Time a member out (Discord's built-in mute).")
    @app_commands.describe(member="Who to mute", minutes="How many minutes", reason="Why")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = None):
        until = datetime.timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)

        embed = result_embed(f"Timed Out for {minutes} min", member, interaction.user, reason, RED)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Delete a bunch of recent messages.")
    @app_commands.describe(amount="How many messages to delete (max 100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        amount = min(amount, 100)
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)

    @app_commands.command(description="Warn a member (sends them a DM).")
    @app_commands.describe(member="Who to warn", reason="What for")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        embed = result_embed("Member Warned", member, interaction.user, reason, discord.Color.orange())
        await interaction.response.send_message(embed=embed)

        try:
            await member.send(f"You were warned in **{interaction.guild.name}**: {reason}")
        except discord.Forbidden:
            # Their DMs are closed. Nothing we can do about that.
            await interaction.followup.send("(Couldn't DM them — their DMs are closed.)", ephemeral=True)

    # One handler for every command in this cog. Keeps the "you're not allowed"
    # message consistent instead of repeating it five times.
    async def cog_app_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            msg = "You don't have permission to use that command."
        else:
            msg = f"Something went wrong: {error}"

        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
