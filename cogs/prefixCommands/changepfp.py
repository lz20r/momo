import discord
import sys
import difflib
import requests
from discord.ext import commands 
from discord.ext.commands import CommandNotFound
import discord as prefix
from discord.ui import Select, View, Button, button

class Changepfp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def changepfp(self, ctx, url: str):
        allowed_ids = [298704465178001418, 1033160523044376616]
        if ctx.author.id not in allowed_ids:
            await ctx.send("You are not authorized to use this command.")
            return
        
        try:
            async with ctx.typing():
                response = requests.get(url)
                if response.status_code == 200:
                    image_data = response.content
                    await self.bot.user.edit(avatar=image_data)
                    await ctx.send("Avatar changed successfully!")
                else:
                    await ctx.send("Failed to download image: Status code {}.".format(response.status_code))
        except Exception as e:
            await ctx.send("An error occurred while changing the avatar: {}".format(e))

async def setup(bot):
    await bot.add_cog(Changepfp(bot))
