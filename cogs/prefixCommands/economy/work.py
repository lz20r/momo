import random 
import discord  
from discord.ext import commands

from cogs.Events.economySystem import EconomySystem

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot) 
        
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
    await bot.add_cog(Work(bot))
