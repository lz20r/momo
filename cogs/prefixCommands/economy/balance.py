import random 
import discord  
from discord.ext import commands

from cogs.Events.economySystem import EconomySystem

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot)

    @commands.command(name='saldo', aliases=['bal'])
    async def balance(self, ctx): 
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id) 
        user_balance = self.economy_system.get_balance(user_id, guild_id)
        if user_balance is not None:
            embed = discord.Embed(title="Saldo", description=f"Tu saldo es de {user_balance} monedas.")
            embed.set_footer(text=f"{self.bot.user.name}'s Balance System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description=f"No se encontró su saldo.")
            embed.set_footer(text=f"{self.bot.user.name}'s Balance System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            
async def setup(bot):  
    await bot.add_cog(Balance(bot))
