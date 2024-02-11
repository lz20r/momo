# balance_cog.py

import discord
from discord.ext import commands
from .economyutils import EconomyUtils

class balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_utils = EconomyUtils(bot)

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        user_data = self.economy_utils.load_economy_data(ctx.guild.id, user_id)
        embed = discord.Embed(title="💰 Balance", description=f'Tu balance actual es: **{user_data["balance"]}** monedas.', color=0x00ff00)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(balance(bot))
