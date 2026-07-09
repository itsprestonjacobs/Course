import datetime
import time

import discord
from discord import app_commands
from discord.ext import commands

import economy_db as db


def xp_for_level(level):
    return 5 * (level ** 2) + 50 * level + 100


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_xp = {}       # user_id -> timestamp, to stop XP farming

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        now = time.time()
        if now - self.last_xp.get(message.author.id, 0) < 60:
            return              # earned XP in the last minute — skip
        self.last_xp[message.author.id] = now

        db.add(message.author.id, coins=1, xp=5)
        stats = db.get(message.author.id)
        if stats["xp"] >= xp_for_level(stats["level"]):
            new_level = stats["level"] + 1
            db.set_level(message.author.id, new_level)
            await message.channel.send(
                f"🎉 {message.author.mention} reached **level {new_level}**!")

    @app_commands.command(description="Check your balance and level.")
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        s = db.get(member.id)
        embed = discord.Embed(title=f"{member.display_name}'s stats", color=discord.Color.gold())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="💰 Coins", value=s["coins"])
        embed.add_field(name="⭐ Level", value=s["level"])
        embed.add_field(name="✨ XP", value=f"{s['xp']} / {xp_for_level(s['level'])}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Claim your daily coins.")
    async def daily(self, interaction: discord.Interaction):
        today = datetime.date.today().isoformat()
        if db.get(interaction.user.id)["last_daily"] == today:
            await interaction.response.send_message(
                "You already claimed your daily today. Come back tomorrow!", ephemeral=True)
            return
        db.add(interaction.user.id, coins=100)
        db.set_daily(interaction.user.id, today)
        await interaction.response.send_message("💰 You claimed **100** daily coins!")

    @app_commands.command(description="Give coins to another member.")
    @app_commands.describe(member="Who to pay", amount="How much")
    async def pay(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if amount <= 0:
            await interaction.response.send_message("Amount must be positive.", ephemeral=True)
            return
        if db.get(interaction.user.id)["coins"] < amount:
            await interaction.response.send_message("You don't have enough coins.", ephemeral=True)
            return
        db.add(interaction.user.id, coins=-amount)
        db.add(member.id, coins=amount)
        await interaction.response.send_message(
            f"💸 {interaction.user.mention} paid {member.mention} **{amount}** coins!")

    @app_commands.command(description="Show the richest members.")
    async def leaderboard(self, interaction: discord.Interaction):
        lines = []
        for i, (user_id, coins, level) in enumerate(db.top(10), start=1):
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f"User {user_id}"
            lines.append(f"**{i}.** {name} — 💰 {coins} (lvl {level})")
        embed = discord.Embed(title="🏆 Leaderboard", description="\n".join(lines) or "No data yet.",
                              color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Economy(bot))
