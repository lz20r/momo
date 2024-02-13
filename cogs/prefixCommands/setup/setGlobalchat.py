import os
import json
import discord
from discord.ext import commands

class setMgchat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.momochat_dir = 'Momo Data/Momo Global Chat'
        self.momochat_file = os.path.join(self.momochat_dir, 'MomoGlobalchat.json')
        self.color_pastel = 0xFFC0CB
        
        if not os.path.exists(self.momochat_dir):
            os.makedirs(self.momochat_dir)

    def loadmomochatconfig(self):
        if os.path.exists(self.momochat_file):
            with open(self.momochat_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def savemomochatconfig(self, config):
        with open(self.momochat_file, "w") as f:
            json.dump(config, f, indent=4)

    @commands.command(name='momochat', aliases=['momocg', 'mgchat'])
    @commands.has_permissions(administrator=True)
    async def globalchat(self, ctx, action=None, channel: discord.TextChannel = None):
        momoprefixes = await self.bot.get_prefix(ctx.message)
        momoprefix = momoprefixes[0] if momoprefixes else None

        if action is None:
            embed = discord.Embed(
                title="Momo Global Chat",
                description=f"<:momopushistik:1205995023209078827> Invalid action. Here's how to use it:\n"
                f"```Momo Usage: {momoprefix}mgchat set <channel>\n"
                f"Momo Example: {momoprefix}mgchat remove <channel>```",
                color=self.color_pastel 
            )
            embed.set_thumbnail(url=ctx.guild.icon.url),
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)           

        if action == "set":
            if channel is None:
                embed = discord.Embed(  
                    description="<:momowarn:1206682132311842878> Please specify a channel to set for Momo Global Chat." 
                )
                embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)  
                await ctx.send(embed=embed) 
                return
            
            channel_id = channel.id if isinstance(channel, discord.TextChannel) else channel

            momochatconfig = self.loadmomochatconfig()
            momochatconfig[str(ctx.guild.id)] = channel_id
            self.savemomochatconfig(momochatconfig)
            embed = discord.Embed( 
                description=f"<:momostar:1206265916472692839> Successfully set {channel.mention} as the Momo Global Chat channel." 
            ) 
            embed.set_thumbnail(url=ctx.guild.icon.url),
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)            
            await ctx.send(embed=embed)   
            
        elif action == "remove":
            momochatconfig = self.loadmomochatconfig()
            if str(ctx.guild.id) in momochatconfig:
                removed_channel_id = momochatconfig.pop(str(ctx.guild.id))
                self.savemomochatconfig(momochatconfig)
                removed_channel = self.bot.get_channel(removed_channel_id)
                if removed_channel:
                    embed = discord.Embed( description=f"<:momostar:1206265916472692839> Successfully removed {removed_channel.mention} as the Momo Global Chat channel.")
                    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)             
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f"<:momostar:1206265916472692839> Successfully removed channel with ID `{removed_channel_id}` as the Momo Global Chat channel.")
                    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)  
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description="<:momowarn:1206682132311842878> Momo Global Chat is not configured yet. Please try again.")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Momo Global Chat",
                description=f"<:momopushistik:1205995023209078827> Invalid action. Here's how to use it:\n"
                f"```Momo Usage: {momoprefix}mgchat set <channel>\n"
                f"Momo Example: {momoprefix}mgchat remove <channel>```",
                color=self.color_pastel 
            )
            embed.set_thumbnail(url=ctx.guild.icon.url),
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(setMgchat(bot))
