import random 
import discord  
from discord.ext import commands

from cogs.Events.economySystem import EconomySystem

class Withdraw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot) 
        
    @commands.command(name='withdraw', aliases=['withd'])
    async def withdraw(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        user_name = str(ctx.author.name)
        guild_name = str(ctx.guild.name)
        self.economy_system.remove_coins(user_id, guild_id, amount)
        embed = discord.Embed(title="Retiro", description=f"{user_name} at {guild_name} Has retirado {amount} monedas.") 
        embed.set_footer(text=f"{self.bot.user.name}'s Work System")
        embed.set_thumbnail(url=ctx.author.avatar.url)        
        await ctx.send(embed=embed)
      
async def setup(bot):  
    bot.max_deposit = 10000000  # Debe ser un número, no una cadena
    await bot.add_cog(Withdraw(bot)) 
