import discord
from discord.ext import commands

class Isolate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.command(name="isolate", aliases=["is"])
    async def isolate(self, ctx):
        """Isolates the user from the server."""
        await ctx.message.delete()
        if ctx.author.voice is not None and ctx.author.voice.channel is not None:
            await ctx.author.edit(voice_channel=None)
            await ctx.send(f"{ctx.author.mention} has been isolated.")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not in a voice channel.")

    @commands.command(name="unisolate", aliases=["unis"])
    async def unisolate(self, ctx):
        """Unisolates the user from the server."""
        await ctx.message.delete()
        if ctx.author.voice is not None and ctx.author.voice.channel is not None:
            await ctx.author.edit(voice_channel=ctx.author.voice.channel)
            await ctx.send(f"{ctx.author.mention} has been unisolated.")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not in a voice channel.")
    
async def setup(bot):
    await bot.add_cog(Isolate(bot))
