import discord
import os
from discord import Embed
from discord.ext import commands
from discord.ui import View, Button

class Ping(commands.Cog):

   def __init__(self, bot):
      self.bot = bot 

   @commands.command(name='ping', aliases=['p', 'latency', 'lat'] ) 
   async def ping(self, ctx):
      """Check for a response from the bot"""
      try:
         ping = round(self.bot.latency * 1000)
         embed = discord.Embed(
            description=(f'Latency: {ping}ms') 
         )
         await ctx.send(embed=embed)
      except:
         embed = discord.Embed(
            description=(f'**{os.error}** `Something went wrong`')
         )
         await ctx.send(embed=embed)
      finally:
         print(f"{ctx.author} has executed {ctx.command} command in {ctx.guild}")

async def setup(bot): 
   await bot.add_cog(Ping(bot)) 

  