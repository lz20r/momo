import random
import discord
from discord.ext import commands
from cogs.Events.economySystem import EconomySystem

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot)

    @commands.command(name='trabajar', aliases=['work'])
    @commands.cooldown(1, 180, commands.BucketType.user)  # Cooldown de 3 minutos por usuario
    async def work(self, ctx):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        earnings = random.randint(10, 100)
        self.economy_system.add_coins(user_id, guild_id, earnings)
        embed = discord.Embed(title="Trabajo", description=f"{ctx.author.display_name} has trabajado y ganado {earnings} monedas.")
        embed.set_footer(text=f"Sistema de Trabajo de {self.bot.user.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed, delete_after=120) 
        ctx.message.delete(delay=120)

    # @work.error
    # async def work_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         # Convertir el tiempo de espera a minutos y redondear hacia arriba
    #         wait_time = error.retry_after / 60  # Convertir de segundos a minutos
    #         if wait_time < 1:
    #             message = f"Tienes que esperar menos de un minuto para volver a trabajar."
    #         else:
    #             message = f"Tienes que esperar {wait_time:.1f} minutos para volver a trabajar."
            
    #         embed = discord.Embed(title="Aviso", description=message)
    #         embed.set_footer(text=f"Sistema de Trabajo de {self.bot.user.display_name}")
    #         await ctx.send(embed=embed)
    #     else:
    #         raise error

async def setup(bot):
    await bot.add_cog(Work(bot))
