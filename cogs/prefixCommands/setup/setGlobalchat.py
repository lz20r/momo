import os
import json
import discord
from discord.ext import commands

class setMgchat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.globalchat_dir = 'Momo Data/Momo Global Chat'
        self.globalchat_file = os.path.join(self.globalchat_dir, 'MomoGlobalchat.json')
        self.color_pastel = 0xFFC0CB
        
        if not os.path.exists(self.globalchat_dir):
            os.makedirs(self.globalchat_dir)

    def load_global_chat_config(self):
        if os.path.exists(self.globalchat_file):
            with open(self.globalchat_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_global_chat_config(self, config):
        with open(self.globalchat_file, "w") as f:
            json.dump(config, f, indent=4)

    @commands.command(name='momochat', aliases=['momocg', 'mgchat'])
    @commands.has_permissions(administrator=True)
    async def globalchat(self, ctx, action=None, channel: discord.TextChannel = None):
        user_prefixes = await self.bot.get_prefix(ctx.message)
        user_prefix = user_prefixes[0] if user_prefixes else None

        if action is None:
            embed = discord.Embed(
                title="Momo Global Chat",
                description=f"<:momopushistik:1205995023209078827> Invalid action. Here's how to use it:\n"
                f"```Momo Usage: {user_prefix}mgchat set <channel>\n"
                f"Momo Example: {user_prefix}mgchat remove <channel>```",
                color=self.color_pastel 
            )

        if action == "set":
            if channel is None:
                embed = discord.Embed(  
                    description="<:momowarn:1206682132311842878> Please specify a channel to set for Momo Global Chat." 
                )
                await ctx.send(embed=embed) 
                return
            
            channel_id = channel.id if isinstance(channel, discord.TextChannel) else channel

            global_chat_config = self.load_global_chat_config()
            global_chat_config[str(ctx.guild.id)] = channel_id
            self.save_global_chat_config(global_chat_config)
            embed = discord.Embed( 
                description=f"<:momostar:1206265916472692839> Successfully set {channel.mention} as the Momo Global Chat channel." 
            ) 
            await ctx.send(embed=embed)   
            
        elif action == "remove":
            global_chat_config = self.load_global_chat_config()
            if str(ctx.guild.id) in global_chat_config:
                removed_channel_id = global_chat_config.pop(str(ctx.guild.id))
                self.save_global_chat_config(global_chat_config)
                removed_channel = self.bot.get_channel(removed_channel_id)
                if removed_channel:
                    embed = discord.Embed( description=f"<:momostar:1206265916472692839> Successfully removed {removed_channel.mention} as the Momo Global Chat channel.")
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(description=f"<:momostar:1206265916472692839> Successfully removed channel with ID `{removed_channel_id}` as the Momo Global Chat channel.")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description="<:momowarn:1206682132311842878> Momo Global Chat is not configured yet. Please try again.")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Momo Global Chat",
                description=f"<:momopushistik:1205995023209078827> Invalid action. Here's how to use it:\n"
                f"```Momo Usage: {user_prefix}mgchat set <channel>\n"
                f"Momo Example: {user_prefix}mgchat remove <channel>```",
                color=self.color_pastel 
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(setMgchat(bot))
