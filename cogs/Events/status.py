import discord
from discord.ext import commands, tasks
from itertools import cycle

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.status = cycle([  
            '💞・host panel.cinammon.es', 
            '💞・m.help to get information',
            '💞・{guild_count} servers',
            '💞・{channel_count} channels'
            '💞・{member_count} members',
            
        ]) 
        
    @tasks.loop(seconds=3.0)
    async def update_status(self):
        new_status = next(self.status) 
        if "{guild_count}" in new_status:
            new_status = new_status.format(guild_count=len(self.bot.guilds))
        elif "{member_count}" in new_status:
            member_count = sum(guild.member_count for guild in self.bot.guilds)
            new_status = new_status.format(member_count=member_count)
        elif "{channel_count}" in new_status:
            channel_count = sum(len(guild.channels) for guild in self.bot.guilds)
            new_status = new_status.format(channel_count=channel_count)
        
        await self.bot.change_presence(activity=discord.CustomActivity(name=new_status), status=discord.Status.idle)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.update_status.start()
        

async def setup(bot):
    await bot.add_cog(Status(bot))
