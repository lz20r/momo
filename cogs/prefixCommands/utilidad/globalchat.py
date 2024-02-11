import os
import json
from sys import prefix
import discord
from discord.ext import commands

class GlobalChat():
    def __init__(self, bot, ctx):
        self.bot = bot
        self.data_folder = "Momo Data"
        os.makedirs(self.data_folder, exist_ok=True)
        self.file_path = os.path.join(self.data_folder, 'Momoglobalchat.json')
        self.color_pastel = 0xFFC0CB
        
        try:
            with open(self.json_file_path, 'r') as f: 
                self.globalchat = json.load(f)
        except FileNotFoundError:
            self.globalchat = {}        
        
        @commands.command(name='globalchat', aliases=['global'])
        @commands.has_permissions(administrator=True)
        async def globalchat(ctx, action=None, channel: discord.TextChannel = None):
                prefix = {await self.bot.get_prefix(ctx.message)} 
                def get_prefix(client, message):
                    return prefix
                
                if action is None:
                    user_prefixes = get_prefix(self.bot, ctx)
                    user_prefix = ''.join(user_prefixes) if user_prefixes else None
                    embed = discord.Embed(title="globalchat command", description=f"This command can talk with other user global\n```Syntax: {user_prefix}globalchat set <channel>\nExample: {user_prefix}globalchat set #general```")
                    await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions(replied_user=False))
                    return
    
                if action == "set":
                    if channel is None:
                        embed = discord.Embed(description=f'<:launted:1203119545213128735> provide the channel to set.')
                        await ctx.send(embed=embed)
                        return
                    
                    if isinstance(channel, discord.TextChannel):
                        channel_id = channel.id
                    else:
                        channel_id = channel
    
                    global_chat_config = load_global_chat_config()
                    global_chat_config[str(ctx.guild.id)] = channel_id
                    save_global_chat_config(global_chat_config)
                    embed = discord.Embed(description=f'<:momocorrect:1206016202745454613>  **successfully** chat global set to <#{channel_id}>.')
                    await ctx.send(embed=embed)
                elif action == "remove":
                    global_chat_config = load_global_chat_config()
                    if str(ctx.guild.id) in global_chat_config:
                        del global_chat_config[str(ctx.guild.id)]
                        save_global_chat_config(global_chat_config)
                        embed = discord.Embed(description=f'<:momocorrect:1206016202745454613>  **successfully** chat global removed.')
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(description=f'<:launted:1203119545213128735> **chat global** is not configured.')
                        await ctx.send(embed=embed)
                else:
                    user_prefixes = get_prefix(client, ctx)
                    user_prefix = ''.join(user_prefixes) if user_prefixes else None
                    embed = discord.Embed(title="globalchat command", description=f"This command can talk with other user global\n```Syntax: {user_prefix}globalchat set <channel>\nExample: {user_prefix}globalchat set #general```")
                    await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions(replied_user=False))
                    return
                
                @commands.Cog.listener()
                async def on_message(self, message):
                    if message.channel.id == global_chat_config[str(message.guild.id)]:
                        await message.delete()
                        embed = discord.Embed(description=message.content, color=self.color_pastel)
                        await message.channel.send(embed=embed)
                def load_global_chat_config():
                    with open(self.file_path, 'r') as f:
                        return json.load(f)
                def save_global_chat_config(config):
                    with open(self.file_path, 'w') as f:
                        json.dump(config, f)
async def setup(bot):
    await bot.add_cog(GlobalChat(bot))

