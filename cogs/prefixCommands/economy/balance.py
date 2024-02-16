import os
import json
import discord
from discord.ext import commands 
from .economyutils import EconomyUtils 

class EconomyCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.economy_utils = EconomyUtils(bot) 

    def load_economy_data(self, guild_id, user_id):
        user_data = self.economy_utils.load_economy_data(guild_id, user_id)
        return user_data
    
    def save_economy_data(self, guild_id, user_id):
        self.economy_utils.save_economy_data(guild_id, user_id)
        return
    
    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        user_data = self.economy_utils.load_economy_data(ctx.guild.id, user_id)
        embed = discord.Embed(title="💰 Balance", description=f'Tu balance actual es: **{user_data["balance"]}** monedas.', color=0x00ff00)
        await ctx.send(embed=embed)

# Este fragmento es necesario para cargar la extensión
async def setup(bot):
    await bot.add_cog(EconomyCommands(bot))
