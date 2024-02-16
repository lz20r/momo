# deposit_cog.py
import os
import discord
from discord.ext import commands
from .economyutils import EconomyUtils


class Deposit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_utils = EconomyUtils(bot)  
        
    def load_economy_data(self, user_id):
        user_data = self.economy_utils.load_economy_data(user_id)
        return user_data
    
    def save_economy_data(self, user_data, user_id):
        self.economy_utils.save_economy_data(user_data, user_id)
        return user_data
        
    @commands.command(name="deposit", aliases=["dep"])
    async def deposit(self, ctx, amount: int):
        if amount <= 0:
            embed = discord.Embed(title="Error", description='Por favor, ingresa una cantidad válida.', color=0xff0000)
            await ctx.send(embed=embed)
            return

        user_id = str(ctx.author.id)
        user_data = self.economy_utils.load_economy_data( user_id )
        user_data["balance"] += amount
        self.save_economy_data(user_data)
        embed = discord.Embed(title="💸 Depósito", description=f'Has depositado **{amount}** monedas.', color=0x00ff00)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Deposit(bot))
