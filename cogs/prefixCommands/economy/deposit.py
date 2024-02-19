import random 
import discord  
from discord.ext import commands

from cogs.Events.economySystem import EconomySystem

class Deposit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot)
        self.max_deposit = 1000  


    @commands.command(name='depositar', aliases=['dep'])
    async def deposit(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        guild_name = str(ctx.guild.name)
        user_name = str(ctx.author.name)
        
        if amount <= 0:
            embed = discord.Embed(title="Información", description=f"{user_name} en {guild_name}, por favor, introduce una cantidad válida para depositar.")
            embed.set_footer(text=f"{self.bot.user.name}'s Deposit System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

        current_balance = self.economy_system.get_balance(user_id, guild_id)
        new_balance = current_balance + amount

        if new_balance > 1000:
            embed = discord.Embed(title="Información", description=f"{user_name} en {guild_name}, no puedes tener más de 1000 monedas en total. Tu saldo actual es de {current_balance} monedas. Intenta depositar una cantidad menor.")
            embed.set_footer(text=f"{self.bot.user.name}'s Deposit System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

        # Añade las monedas y actualiza el saldo en la base de datos
        self.economy_system.add_coins(user_id, guild_id, amount)

        embed = discord.Embed(title="Depósito Realizado", description=f"{user_name} en {guild_name}, has depositado {amount} monedas en tu cuenta exitosamente. Tu nuevo saldo es de {new_balance} monedas.")
        embed.set_footer(text=f"{self.bot.user.name}'s Deposit System")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
   
async def setup(bot):  
    bot.max_deposit = 10000000  # Debe ser un número, no una cadena
    await bot.add_cog(Deposit(bot))
