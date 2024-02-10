import discord
from discord.ext import commands

class Isolate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.command("isolate", aliases=["is"])
    async def isolate(self, ctx):
        """Isolates the user from the server."""
        await ctx.message.delete()
        await ctx.author.edit(voice_channel=None)
        await ctx.send(f"{ctx.author.mention} has been isolated.")
        
    @commands.command("unisolate", aliases=["unis"])
    async def unisolate(self, ctx):
        """Unisolates the user from the server."""
        await ctx.message.delete()
        await ctx.author.edit(voice_channel=ctx.author.voice.channel)
        await ctx.send(f"{ctx.author.mention} has been unisolated.")
    
async def setup(bot):
    await bot.add_cog(Isolate(bot))
