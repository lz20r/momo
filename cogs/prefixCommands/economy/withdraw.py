import random 
import discord  
from discord.ext import commands 
from cogs.Events.economySystem import EconomySystem

class Withdraw(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot)
        self.max_withdraw = 1000  # Establece el límite máximo de retiro aquí

    @commands.command(name='withdraw', aliases=['withd'])
    async def withdraw(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        user_name = str(ctx.author.name)
        guild_name = str(ctx.guild.name)

        # Verificar si la cantidad es válida
        if amount <= 0:
            embed = discord.Embed(title="Advertencia", description=f"{user_name} en {guild_name}, no puedes retirar una cantidad negativa o cero.")
            embed.set_footer(text=f"{self.bot.user.name}'s Withdraw System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

        # Verificar si la cantidad excede el límite máximo de retiro
        if amount > self.max_withdraw:
            embed = discord.Embed(title="Advertencia", description=f"{user_name} en {guild_name}, el monto máximo que puedes retirar es de {self.max_withdraw} monedas.")
            embed.set_footer(text=f"{self.bot.user.name}'s Withdraw System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

        # Obtener el saldo actual del usuario
        current_balance = self.economy_system.get_balance(user_id, guild_id)

        # Verificar si el usuario tiene suficiente saldo para retirar
        if amount > current_balance:
            embed = discord.Embed(title="Advertencia", description=f"{user_name} en {guild_name}, no puedes retirar más de lo que tienes. Tu saldo actual es de {current_balance} monedas.")
            embed.set_footer(text=f"{self.bot.user.name}'s Withdraw System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

        # Proceder con el retiro si se cumplen las condiciones
        self.economy_system.remove_coins(user_id, guild_id, amount)
        embed = discord.Embed(title="Retiro Exitoso", description=f"{user_name} en {guild_name}, has retirado {amount} monedas exitosamente.")
        embed.set_footer(text=f"{self.bot.user.name}'s Withdraw System")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):  
    await bot.add_cog(Withdraw(bot))
