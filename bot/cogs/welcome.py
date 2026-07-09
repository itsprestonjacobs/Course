import discord
from discord.ext import commands

import settings


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def channel_for(self, guild, key, default):
        name = settings.get(guild.id, key, default)
        return discord.utils.get(guild.text_channels, name=name)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.channel_for(member.guild, "welcome_channel", "welcome")
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

        # Hand out a default "Member" role if one exists.
        role = discord.utils.get(member.guild.roles, name="Member")
        if role and role < member.guild.me.top_role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.channel_for(member.guild, "welcome_channel", "welcome")
        if channel:
            embed = discord.Embed(title=f"Goodbye, {member.name}",
                                  description="We'll miss you!", color=discord.Color.red())
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Welcome(bot))
