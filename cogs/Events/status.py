import discord
import sys
import difflib
from itertools import cycle
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.status = cycle([  
            '💞・hosted in panel.cinammon.es', 
            '💞・m.help to get information',
            '💞・{guild_count} servers'
        ]) 
        
    @tasks.loop(seconds=3.0)
    async def update_status(self):
        new_status = next(self.status) 
        if "{guild_count}" in new_status:
            new_status = new_status.format(guild_count=len(self.bot.guilds))
            await self.bot.change_presence(activity=discord.CustomActivity(name=new_status), status=discord.Status.dnd)
        else:
            await self.bot.change_presence(activity=discord.CustomActivity(name=new_status), status=discord.Status.dnd)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.update_status.start()
        

async def setup(bot):
    await bot.add_cog(Status(bot)) 