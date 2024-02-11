# withdraw_cog.py

import discord
from discord.ext import commands
from .economyutils import load_economy_data, save_economy_data

class Withdraw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="withdraw", aliases=["with"])
    async def withdraw(self, ctx, amount: int):
        if amount <= 0:
            embed = discord.Embed(title="Error", description='Por favor, ingresa una cantidad válida.', color=0xff0000)
            await ctx.send(embed=embed)
            return

        user_id = str(ctx.author.id)
        user_data = load_economy_data(user_id)
        if user_data["balance"] >= amount:
            user_data["balance"] -= amount
            save_economy_data(user_data)
            embed = discord.Embed(title="💸 Retiro", description=f'Has retirado **{amount}** monedas.', color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description='No tienes suficientes monedas para retirar esa cantidad.', color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Withdraw(bot))
