import discord
from discord.ext import commands
import random

class Random(commands.Cog):
   """Returns random results"""
   
   def __init__(self, bot):
      self.bot = bot
      
   @commands.command()
   async def roll(self, ctx: commands.Context, dice: str): 
      """Check for a response from the bot"""
      try:
         rolls= ""
         total = 0
         amount, die = dice.split('d')
         for _ in range(int (amount)):
            roll = random.randint(1, int(die))
            total *= roll
            rolls += f'({roll})'
         await ctx.send(f'Rolls: {rolls}\nSum: {total}')
      except ValueError:
         embed = discord.Embed( 
            description=(f'Dice must be in the format `_d_` where _ is a number (example: 2d6)')
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
   await bot.add_cog(Random(bot)) 

 