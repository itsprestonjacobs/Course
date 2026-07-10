import datetime

import discord
from discord import app_commands
from discord.ext import commands

from config import LOG_CHANNEL

RED = discord.Color.red()
ORANGE = discord.Color.orange()
GREEN = discord.Color.green()


def result_embed(action, target, moderator, reason, color):
    embed = discord.Embed(title=action, color=color, timestamp=datetime.datetime.now())
    embed.add_field(name="Target", value=f"{target}", inline=False)
    embed.add_field(name="Moderator", value=moderator.mention, inline=False)
    if reason is not None:
        embed.add_field(name="Reason", value=reason or "No reason given", inline=False)
    return embed


async def mod_log(guild, embed):
    """Post a copy of every moderation action to the log channel."""
    channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL)
    if channel:
        await channel.send(embed=embed)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def outranks(self, interaction, member):
        """True if the target is ranked equal to or above the moderator."""
        return member.top_role >= interaction.user.top_role

    # ---------- kick / ban / unban ----------
    @app_commands.command(description="Kick a member.")
    @app_commands.describe(member="Who to kick", reason="Why")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction, member: discord.Member, reason: str = None):
        if self.outranks(interaction, member):
            await interaction.response.send_message(
                "You can't kick someone ranked equal to or above you.", ephemeral=True)
            return
        await member.kick(reason=reason)
        embed = result_embed("Member Kicked", member, interaction.user, reason, RED)
        await interaction.response.send_message(embed=embed)
        await mod_log(interaction.guild, embed)

    @app_commands.command(description="Ban a member.")
    @app_commands.describe(member="Who to ban", reason="Why")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction, member: discord.Member, reason: str = None):
        if self.outranks(interaction, member):
            await interaction.response.send_message(
                "You can't ban someone ranked equal to or above you.", ephemeral=True)
            return
        await member.ban(reason=reason)
        embed = result_embed("Member Banned", member, interaction.user, reason, RED)
        await interaction.response.send_message(embed=embed)
        await mod_log(interaction.guild, embed)

    @app_commands.command(description="Unban a user by their ID.")
    @app_commands.describe(user_id="The banned user's ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction, user_id: str):
        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        embed = result_embed("Member Unbanned", user, interaction.user, None, GREEN)
        await interaction.response.send_message(embed=embed)
        await mod_log(interaction.guild, embed)

    # ---------- timeout / untimeout ----------
    @app_commands.command(description="Time a member out (mute) for some minutes.")
    @app_commands.describe(member="Who", minutes="How long", reason="Why")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction, member: discord.Member, minutes: int, reason: str = None):
        await member.timeout(datetime.timedelta(minutes=minutes), reason=reason)
        embed = result_embed(f"Timed Out ({minutes} min)", member, interaction.user, reason, RED)
        await interaction.response.send_message(embed=embed)
        await mod_log(interaction.guild, embed)

    @app_commands.command(description="Remove a member's timeout.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout(self, interaction, member: discord.Member):
        await member.timeout(None)
        embed = result_embed("Timeout Removed", member, interaction.user, None, GREEN)
        await interaction.response.send_message(embed=embed)
        await mod_log(interaction.guild, embed)

    # ---------- purge / slowmode ----------
    @app_commands.command(description="Delete recent messages (max 100).")
    @app_commands.describe(amount="How many")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction, amount: int):
        amount = min(amount, 100)
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)
        embed = result_embed("Messages Purged", f"{len(deleted)} in {interaction.channel.mention}",
                             interaction.user, None, ORANGE)
        await mod_log(interaction.guild, embed)

    @app_commands.command(description="Set slowmode (seconds) on this channel.")
    @app_commands.describe(seconds="Delay between messages, 0 to turn off")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction, seconds: int):
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"Slowmode set to **{seconds}s**.")

    # ---------- lock / unlock ----------
    @app_commands.command(description="Lock this channel (stop @everyone talking).")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message("🔒 Channel locked.")
        await mod_log(interaction.guild,
                      result_embed("Channel Locked", interaction.channel.mention, interaction.user, None, ORANGE))

    @app_commands.command(description="Unlock this channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=None)
        await interaction.response.send_message("🔓 Channel unlocked.")
        await mod_log(interaction.guild,
                      result_embed("Channel Unlocked", interaction.channel.mention, interaction.user, None, GREEN))

    # ---------- nick / role ----------
    @app_commands.command(description="Change a member's nickname.")
    @app_commands.describe(member="Who", nickname="New nickname (leave blank to reset)")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def nick(self, interaction, member: discord.Member, nickname: str = None):
        await member.edit(nick=nickname)
        await interaction.response.send_message(
            f"Changed {member.mention}'s nickname to **{nickname or member.name}**.")

    @app_commands.command(description="Give or remove a role from a member.")
    @app_commands.describe(member="Who", role="Which role to toggle")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role(self, interaction, member: discord.Member, role: discord.Role):
        if role >= interaction.user.top_role:
            await interaction.response.send_message(
                "You can't assign a role equal to or above your own.", ephemeral=True)
            return
        if role in member.roles:
            await member.remove_roles(role)
            action = "Removed"
        else:
            await member.add_roles(role)
            action = "Gave"
        await interaction.response.send_message(f"{action} **{role.name}** {'from' if action=='Removed' else 'to'} {member.mention}.")

    # One friendly handler for every command in this cog.
    async def cog_app_command_error(self, interaction, error):
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
