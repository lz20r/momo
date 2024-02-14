
import os
import re
import json
import time
import timeit
import discord
from datetime import datetime
from discord.ext import commands 


class momochatEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.momochatdir = 'Momo Data/Momo Global Chat'
        self.momochatfile = os.path.join(self.momochatdir, 'MomoGlobalchat.json')
        self.ahora = datetime.now().strftime("%d/%m %H:%M")
        if not os.path.exists(self.momochatdir):
            os.makedirs(self.momochatdir)

    def loadmomochatconfig(self):
        if os.path.exists(self.momochatfile):
            with open(self.momochatfile, "r") as f:
                return json.load(f)
        else:
            return {}

    def savemomochatconfig(self, config):
        with open(self.momochatfile, "w") as f:
            json.dump(config, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return 
            
        momochatconfig = self.loadmomochatconfig()
        momomessagechid = message.channel.id

        if momomessagechid in momochatconfig.values():
            momoauthorname = message.author.name
            momoauthoricon = message.author.avatar.url if message.author.avatar else discord.Embed.Empty
            momoservername = message.guild.name
            created_at = message.created_at
            formatted_created_at = discord.utils.format_dt(created_at, 'R')
            server_icon = message.guild.icon.url if message.guild.icon else discord.Embed.Empty
            embed = discord.Embed(title=f"<:momostar:1206265916472692839> {self.bot.user.name}")
            embed.set_author(name=momoauthorname, icon_url=momoauthoricon)
            embed.set_footer(text=f'{momoservername}', icon_url=f'{server_icon}')
            embed.timestamp = datetime.now()
            embed.set_thumbnail(url=momoauthoricon) 

            momolinks = re.findall(r'https?://[^\s]+', message.content)
 
            momoimagelinks = [link for link in momolinks if re.search(r'\.(jpg|png|jpeg|gif)$', link)]

            if momoimagelinks:
                for momolink in momoimagelinks:
                    embed.set_image(url=momolink)
                    for momochannelid in momochatconfig.values():
                        momoglobalchannel = self.bot.get_channel(momochannelid)
                        if momoglobalchannel:
                            await momoglobalchannel.send(embed=embed)
            else:
                embed.description = f"""
                <:momostar:1206265916472692839> {message.content} \n 
                <:momostar:1206265916472692839> {formatted_created_at}
                """ 
                for momochannelid in momochatconfig.values():
                    momoglobalchannel = self.bot.get_channel(momochannelid)
                    if momoglobalchannel:
                        await momoglobalchannel.send(embed=embed)
                await message.delete()

async def setup(bot):
    await bot.add_cog(momochatEvent(bot))