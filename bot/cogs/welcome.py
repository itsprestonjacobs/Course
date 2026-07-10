import discord
from discord.ext import commands

import settings
from config import WELCOME_CHANNEL, AUTO_ROLE_NAME


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def welcome_channel(self, guild):
        # Per-server override (set with /set_welcome), else the config default.
        name = settings.get(guild.id, "welcome_channel", WELCOME_CHANNEL)
        return discord.utils.get(guild.text_channels, name=name)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.welcome_channel(member.guild)
        if channel:
            embed = discord.Embed(
                title=f"Welcome, {member.name}! 👋",
                description=f"Hey {member.mention}, welcome to **{member.guild.name}**!\n"
                            "Grab your roles and say hi.",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"You're member #{member.guild.member_count}")
            await channel.send(embed=embed)

        # Auto-assign a starter role if one is configured.
        if AUTO_ROLE_NAME:
            role = discord.utils.get(member.guild.roles, name=AUTO_ROLE_NAME)
            if role and role < member.guild.me.top_role:
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.welcome_channel(member.guild)
        if channel:
            embed = discord.Embed(title=f"Goodbye, {member.name}",
                                  description="We'll miss you!", color=discord.Color.red())
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Welcome(bot))
