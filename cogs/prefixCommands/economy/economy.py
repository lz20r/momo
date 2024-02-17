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

    def register_user(self, user_id, guild_id, username):
        if not self.user_exists(user_id, guild_id):
            sql = "INSERT INTO users (user_id, guild_id, username, balance) VALUES (%s, %s, %s, %s)"
            val = (user_id, guild_id, username, 0)  # Inicializa el balance a 0
            self.cursor.execute(sql, val)
            self.mysql_connection.commit()
        else:
            print("El usuario ya está registrado.")
            return

    def user_exists(self, user_id, guild_id):
        sql = "SELECT COUNT(*) FROM users WHERE guild_id = %s AND user_id = %s"
        val = (user_id, guild_id)
        try:
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()
            return result[0] > 0 if result else False
        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta SQL:", err)
            return False

    def get_balance(self, user_id, guild_id):
        sql = "SELECT balance FROM users WHERE guild_id = %s AND user_id = %s"
        val = (user_id, guild_id)
        try:
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()
            return int(result[0]) if result is not None else None
        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta SQL:", err)
            return None

    def add_coins(self, user_id, guild_id, amount):
        if self.user_exists(user_id, guild_id):
            current_balance = self.get_balance(user_id, guild_id)
            if current_balance is None:
                print("No se pudo obtener el balance del usuario.")
                return
            new_balance = current_balance + amount
            sql = "UPDATE users SET balance = %s WHERE guild_id = %s AND user_id = %s"
            val = (new_balance, user_id, guild_id)
            try:
                self.cursor.execute(sql, val)
                self.mysql_connection.commit()
            except mysql.connector.Error as err:
                print("Error al ejecutar la consulta SQL:", err)
                return
        else:
            print("Usuario no encontrado.")
            return

    def remove_coins(self, user_id, guild_id, amount):
        if self.user_exists(user_id, guild_id):
            current_balance = self.get_balance(user_id, guild_id)
            if current_balance is None:
                print("No se pudo obtener el balance del usuario.")
                return
            new_balance = max(current_balance - amount, 0)  # Ensure balance doesn't go negative
            sql = "UPDATE users SET balance = %s WHERE guild_id = %s AND user_id = %s"
            val = (new_balance, user_id, guild_id)
            try:
                self.cursor.execute(sql, val)
                self.mysql_connection.commit()
            except mysql.connector.Error as err:
                print("Error al ejecutar la consulta SQL:", err)
                return
        else:
            print("Usuario no encontrado.")

    def close(self):
        self.cursor.close()
        self.mysql_connection.close()


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
