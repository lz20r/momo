import random 
import discord  
from discord.ext import commands

from cogs.Events.economySystem import EconomySystem

class Deposit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot)
        self.max_deposit = 10000000  # Debe ser un número, no una cadena


    @commands.command(name='depositar', aliases=['dep'])
    async def deposit(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id) 
        guild_name = str(ctx.guild.name)
        user_name = str(ctx.author.name)
        
        if amount <= 0:
            embed = discord.Embed(title="Error", description=f"{user_name} en {guild_name}, por favor, introduce una cantidad válida para depositar.")
            embed.set_footer(text=f"{self.bot.user.name}'s Deposit System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return
        elif amount > self.max_deposit:  # Compara con un número, no una cadena
            embed = discord.Embed(title="Error", description=f"{user_name} en {guild_name}, no puedes depositar más de {self.max_deposit} monedas.")
            embed.set_footer(text=f"{self.bot.user.name}'s Deposit System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return
        else:
            self.economy_system.add_coins(user_id, guild_id, amount)
            embed = discord.Embed(title="Depósito", description=f"{user_name} en {guild_name}, has depositado {amount} monedas en tu cuenta.")
            embed.set_footer(text=f"{self.bot.user.name}'s Deposit System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed) 
        
async def setup(bot):  
    bot.max_deposit = 10000000  # Debe ser un número, no una cadena
    await bot.add_cog(Deposit(bot))
