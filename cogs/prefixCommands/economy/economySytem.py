import os
import json
import random 
import discord
import mysql.connector
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv() 
MOMO_HOST = os.getenv('MOMO_HOST') 
MOMO_PORT = os.getenv('MOMO_PORT') 
MOMO_USER = os.getenv('MOMO_USER')
MOMO_PASS = os.getenv('MOMO_PASS')
MOMO_NAME = os.getenv('MOMO_NAME')

class EconomySystem:
    def __init__(self, bot):
        self.bot = bot
        self.mysql_connection = mysql.connector.connect(
            host=MOMO_HOST,
            port=MOMO_PORT,
            user=MOMO_USER,
            password=MOMO_PASS, 
            database=MOMO_NAME
        )
        self.cursor = self.mysql_connection.cursor()

    def register_user(self, guild_id, user_id, username):
        if not self.user_exists(guild_id, user_id):
            sql = "INSERT INTO users (guild_id, user_id, username, balance) VALUES (%s, %s, %s, %s)"
            val = (guild_id, user_id, username, 0)  
            self.cursor.execute(sql, val)
            self.mysql_connection.commit()
        else:
            print("El usuario ya está registrado.")
            return

    def user_exists(self, guild_id, user_id):
        sql = "SELECT COUNT(*) FROM users WHERE guild_id = %s AND user_id = %s"
        val = (guild_id, user_id)
        try:
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()
            return result[0] > 0 if result else False
        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta SQL:", err)
            return False

    def get_balance(self, guild_id, user_id):
        sql = "SELECT balance FROM users WHERE guild_id = %s AND user_id = %s"
        val = (guild_id, user_id)
        try:
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta SQL:", err)
            return None

    def add_coins(self, guild_id, user_id, amount):
        if self.user_exists(guild_id, user_id):
            current_balance = self.get_balance(guild_id, user_id)
            new_balance = current_balance + amount
            sql = "UPDATE users SET balance = %s WHERE guild_id = %s AND user_id = %s"
            val = (new_balance, guild_id, user_id)
            try:
                self.cursor.execute(sql, val)
                self.mysql_connection.commit()
            except mysql.connector.Error as err:
                print("Error al ejecutar la consulta SQL:", err)
                return
        else:
            print("Usuario no encontrado.")
            return

    def remove_coins(self, guild_id, user_id, amount):
        if self.user_exists(guild_id, user_id):
            current_balance = self.get_balance(guild_id, user_id)
            new_balance = max(current_balance - amount, 0)  # Ensure balance doesn't go negative
            sql = "UPDATE users SET balance = %s WHERE guild_id = %s AND user_id = %s"
            val = (new_balance, guild_id, user_id)
            try:
                self.cursor.execute(sql, val)
                self.mysql_connection.commit()
            except mysql.connector.Error as err:
                print("Error al ejecutar la consulta SQL:", err)
                return
        else:
            print("Usuario no encontrado.")  
            return

    def close(self):
        self.cursor.close()
        self.mysql_connection.close()


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot)
        self.max_deposit = str(10000000)

    @commands.command(name='saldo', aliases=['bal'])
    async def balance(self, ctx): 
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id) 
        user_name = str(ctx.author.name)
        guild_name = str(ctx.guild.name)
        user_balance = self.economy_system.get_balance(guild_id, user_id)
        if user_balance is not None:
            embed = discord.Embed(title="Saldo", description=f"Tu saldo es de {user_balance} monedas.")
            embed.set_footer(text=f"{self.bot.user.name}'s Balance System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description=f"{user_name} en {guild_name}, No se encontró su saldo.")
          
    @commands.command(name='depositar', aliases=['dep'])
    async def deposit(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id) 
        guild_name = str(ctx.guild.name)
        user_name = str(ctx.author.name)
        self.max_deposit = 10000000
        
        if amount <= 0:
            embed = discord.Embed(title="Error", description=f"{user_name} en {guild_name}, por favor, introduce una cantidad válida para depositar.")
            embed.set_footer(text=f"{self.bot.user.name}'s Deposit System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return
        elif amount > self.max_deposit:
            embed = discord.Embed(title="Error", description=f"{user_name} en {guild_name}, no puedes depositar más de {self.max_deposit} monedas.")
            embed.set_footer(text=f"{self.bot.user.name}'s Deposit System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return
        else:
            self.economy_system.add_coins(guild_id, user_id, amount)
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
        self.economy_system.remove_coins(guild_id, user_id, amount)
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
        self.economy_system.add_coins(guild_id, user_id, earnings)
        embed = discord.Embed(title="Trabajo", description=f"{user_name} at {guild_name} Has trabajado y ganado {earnings} monedas.")
        embed.set_footer(text=f"{self.bot.user.name}'s Work System")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):  
    bot.max_deposit = str(10000000),
    await bot.add_cog(Economy(bot))
