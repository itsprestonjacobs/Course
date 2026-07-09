import discord
from discord.ext import commands

# Add your own words here. Keep it lowercase.
BANNED_WORDS = ["scam", "free nitro"]


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_message = {}      # user_id -> their last message (simple anti-spam)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        # Leave staff alone.
        if message.author.guild_permissions.manage_messages:
            return

        content = message.content.lower()

        # Invite links
        if "discord.gg/" in content or "discord.com/invite" in content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, no invite links!", delete_after=5)
            return

        # Banned words
        if any(word in content for word in BANNED_WORDS):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, watch your language! ⚠️", delete_after=5)
            return

        # Repeated-message spam
        if self.last_message.get(message.author.id) == content and content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, stop spamming!", delete_after=5)
        self.last_message[message.author.id] = content


async def setup(bot):
    await bot.add_cog(AutoMod(bot))
