# deposit_cog.py

import discord
from discord.ext import commands
from .economyutils import load_economy_data, save_economy_data

class Deposit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deposit", aliases=["dep"])
    async def deposit(self, ctx, amount: int):
        if amount <= 0:
            embed = discord.Embed(title="Error", description='Por favor, ingresa una cantidad válida.', color=0xff0000)
            await ctx.send(embed=embed)
            return

        user_id = str(ctx.author.id)
        user_data = load_economy_data(user_id)
        user_data["balance"] += amount
        save_economy_data(user_data)
        embed = discord.Embed(title="💸 Depósito", description=f'Has depositado **{amount}** monedas.', color=0x00ff00)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Deposit(bot))
