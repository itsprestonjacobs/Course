import discord
from discord.ext import commands

import settings


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def log_channel(self, guild):
        name = settings.get(guild.id, "log_channel", "mod-logs")
        return discord.utils.get(guild.text_channels, name=name)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return
        channel = self.log_channel(message.guild)
        if not channel:
            return
        embed = discord.Embed(title="🗑️ Message Deleted", description=message.content or "*(no text)*",
                              color=discord.Color.red(), timestamp=discord.utils.utcnow())
        embed.add_field(name="Author", value=message.author.mention)
        embed.add_field(name="Channel", value=message.channel.mention)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content or not before.guild:
            return
        channel = self.log_channel(before.guild)
        if not channel:
            return
        embed = discord.Embed(title="✏️ Message Edited", color=discord.Color.orange(),
                              timestamp=discord.utils.utcnow())
        embed.add_field(name="Before", value=before.content or "*(empty)*", inline=False)
        embed.add_field(name="After", value=after.content or "*(empty)*", inline=False)
        embed.add_field(name="Author", value=before.author.mention, inline=False)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.log_channel(member.guild)
        if channel:
            embed = discord.Embed(description=f"📥 {member.mention} **joined**",
                                  color=discord.Color.green(), timestamp=discord.utils.utcnow())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.log_channel(member.guild)
        if channel:
            embed = discord.Embed(description=f"📤 {member.mention} **left**",
                                  color=discord.Color.dark_grey(), timestamp=discord.utils.utcnow())
            await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
