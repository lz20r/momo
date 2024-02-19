import os
import json
import random 
import discord
import mysql.connector
from dotenv import load_dotenv
from discord.ext import commands

from cogs.Events.economySystem import EconomySystem

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot)
        self.max_deposit = 10000000  # Debe ser un número, no una cadena

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
        
    @commands.command(name='trabajar', aliases=['work'])
    async def work(self, ctx):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        user_name = str(ctx.author.name)
        guild_name = str(ctx.guild.name)
        earnings = random.randint(10, 100)  
        self.economy_system.add_coins(user_id, guild_id, earnings)
        embed = discord.Embed(title="Trabajo", description=f"{user_name} at {guild_name} Has trabajado y ganado {earnings} monedas.")
        embed.set_footer(text=f"{self.bot.user.name}'s Work System")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):  
    bot.max_deposit = 10000000  # Debe ser un número, no una cadena
    await bot.add_cog(Economy(bot))
