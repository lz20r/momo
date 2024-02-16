# withdraw_cog.py

import discord
from discord.ext import commands
from .economyutils import EconomyUtils 

class Withdraw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economyutils = EconomyUtils(bot)  
        
    def load_economy_data(self, user_id):
        user_data = self.economyutils.load_economy_data(user_id)
        return user_data
    
    def save_economy_data(self, user_data, user_id):
        self.economyutils.save_economy_data(user_data, user_id)
        return user_data
    
    @commands.command(name="withdraw", aliases=["wd"])
    async def withdraw(self, ctx, amount: int):
        if amount <= 0:
            embed = discord.Embed(title="Error", description='Por favor, ingresa una cantidad válida.', color=0xff0000)
            await ctx.send(embed=embed)
            return

        user_id = str(ctx.author.id)
        user_data = self.load_economy_data(user_id)
        if user_data["balance"] >= amount:
            user_data["balance"] -= amount
            self.save_economy_data(user_data)
            embed = discord.Embed(title="💸 Retiro", description=f'Has retirado **{amount}** monedas.', color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description='No tienes suficientes monedas para retirar esa cantidad.', color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Withdraw(bot))
