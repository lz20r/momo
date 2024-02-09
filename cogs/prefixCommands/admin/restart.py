import discord
import sys
import difflib
import requests
from discord.ext import commands 
from discord.ext.commands import CommandNotFound
import discord as prefix
from discord.ui import Select, View, Button, button

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart", aliases=["reset", "r"])
    async def restart(self, ctx):
        allowed_ids = [298704465178001418, 1033160523044376616]
        author_id = ctx.author.id
        if author_id not in allowed_ids:
            embed = discord.Embed(title="", description="You are not allowed to use the **restart** command!")
            return await ctx.send(embed=embed)
        try:
            embed = discord.Embed(title=" ", description=f"the bot was restarted and was freed from the space that was running in the folder.")
            await ctx.send(embed=embed)
            await self.bot.close()
        except Exception as e:
            pass

async def setup(bot):
    await bot.add_cog(Restart(bot))