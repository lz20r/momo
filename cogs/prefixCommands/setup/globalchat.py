from math import e
import os
import json
import discord
from discord.ext import commands

class GobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.globalchat_dir = 'Momo Data/Momo Global Chat'
        self.globalchat_file = os.path.join(self.globalchat_dir, 'MomoGlobalchat.json')
        self.color_pastel = 0xFFC0CB
        
        if not os.path.exists(self.globalchat_dir):
            os.makedirs(self.globalchat_dir)

    def loadmgchatconfig(self):
        if os.path.exists(self.globalchat_file):
            with open(self.globalchat_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_global_chat_config(self, config):
        with open(self.globalchat_file, "w") as f:
            json.dump(config, f, indent=4)

    @commands.command(name='momochat', aliases=['mgchat'])
    @commands.has_permissions(administrator=True)
    async def globalchat(self, ctx, action=None, channel: discord.TextChannel = None):
        momoprefixes = await self.bot.get_prefix(ctx.message)
        momouserprefix = ''.join(str(momoprefixes)) if momoprefixes else None
        
        if action is None:  
            embed = discord.Embed(
            title="Momo Global Chat",
            description=f"<:momostar:1206265916472692839> Momo chat can join others users from other servers to talk with each other. Here's how to use it:\n"
                        f"```Momo Usage: {momouserprefix}mgchat set <channel>\n"
                        f"Momo Example: {momouserprefix}mgchat set #channel```",
            color=self.color_pastel
            )
            embed.set_footer(text="Momo Global Chat")   
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
            return 
 
        if action == "set":
            if channel is None:
                
                embed = discord.Embed(  
                    description="<:momowarn:1206682132311842878> Please specify a channel to set for Momo Global Chat." 
                )
                await ctx.send(embed=embed) 
                
                momochannel = channel.id if isinstance(channel, discord.TextChannel) else channel

                mgchatconfig = self.loadmgchatconfig()
                
                mgchatconfig[str(ctx.guild.id)] = momochannel
                self.save_global_chat_config(mgchatconfig)
                embed = discord.Embed( 
                    description=f"<:momostar:1206265916472692839> Successfully set {channel.mention} as the Momo Global Chat channel." 
                ) 
                await ctx.send(embed=embed)     
            
                
        elif action == "remove":
            mgchatconfig = self.loadmgchatconfig()
            if str(ctx.guild.id) in mgchatconfig:
                del mgchatconfig[str(ctx.guild.id)]
                self.save_global_chat_config(mgchatconfig)
                embed = discord.Embed( 
                    description=f"<:momostar:1206265916472692839> Successfully removed {channel.mention} as the Momo Global Chat channel." 
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(  
                    description="<:momowarn:1206682132311842878> Momo Global Chat is not configured yet try again\n" 
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Momo Global Chat",
                description=f"<:momopushistik:1205995023209078827> Invalid action. Here's how to use it:\n"
                f"```Momo Usage: {momouserprefix}mgchat set <channel>\n"
                f"Momo Example: {momouserprefix}mgchat remove <channel>```",
                color=self.color_pastel 
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GobalChat(bot))
