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
        author_name = ctx.author.name
        if author_id not in allowed_ids:
            embed = discord.Embed(title="", description="<:mtinfo:1205861978594091109> You are not allowed to use the **restart** command!")
            return await ctx.send(embed=embed, delete_after=10)
        try:
            embed = discord.Embed(description=f"<:mtinfo:1205861978594091109> {author_name} is restarting Momo")
            await ctx.send(embed=embed, delete_after=10)
            await self.bot.close()
        except Exception as e:
            pass

async def setup(bot):
    await bot.add_cog(Restart(bot))
