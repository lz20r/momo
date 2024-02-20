import random
import discord
from discord.ext import commands
from cogs.Events.economySystem import EconomySystem

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot)

    @commands.command(name='trabajar', aliases=['work'])
    @commands.cooldown(1, 86400, commands.BucketType.user)  # Cooldown de 1 día por usuario
    async def work(self, ctx):
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        earnings = random.randint(10, 100)
        self.economy_system.add_coins(user_id, guild_id, earnings)
        embed = discord.Embed(title="Trabajo", description=f"{ctx.author.display_name} has worked and earned {earnings} coins.")
        embed.set_footer(text=f"Sistema de Trabajo de {self.bot.user.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed, delete_after=120)  # Opcional: Puedes aumentar o quitar el tiempo de eliminación
        await ctx.message.delete(delay=120)  # Opcional: Puedes aumentar o quitar el tiempo de eliminación
 

async def setup(bot):
    await bot.add_cog(Work(bot))
