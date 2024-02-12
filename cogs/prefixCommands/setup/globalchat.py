import discord
from discord.ext import commands
import os
import json

class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.globalchat_dir = 'Momo Data'
        self.globalchat_file = os.path.join(self.globalchat_dir, 'globalchat.json')

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

    @commands.command(name='globalchat', aliases=['global'])
    @commands.has_permissions(administrator=True)
    async def globalchat(self, ctx, action=None, channel: discord.TextChannel = None):
        if action is None:
            user_prefixes = self.bot.get_prefix(ctx.message)
            user_prefix = ''.join(user_prefixes) if user_prefixes else None
            embed = discord.Embed(title="globalchat command", description=f"This command can talk with other users globally\n```Syntax: {user_prefix}globalchat set <channel>\nExample: {user_prefix}globalchat set #general```")
            await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions(replied_user=False))
            return

        if action == "set":
            if channel is None:
                embed = discord.Embed(description=f'Please provide the channel to set.')
                await ctx.send(embed=embed)
                return
            
            channel_id = channel.id if isinstance(channel, discord.TextChannel) else channel

            global_chat_config = self.load_global_chat_config()
            global_chat_config[str(ctx.guild.id)] = channel_id
            self.save_global_chat_config(global_chat_config)
            embed = discord.Embed(description=f'**Successfully** set global chat to <#{channel_id}>.')
            await ctx.send(embed=embed)
        elif action == "remove":
            global_chat_config = self.load_global_chat_config()
            if str(ctx.guild.id) in global_chat_config:
                del global_chat_config[str(ctx.guild.id)]
                self.save_global_chat_config(global_chat_config)
                embed = discord.Embed(description=f'**Successfully** removed global chat.')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'**Global chat** is not configured.')
                await ctx.send(embed=embed)
        else:
            user_prefixes = self.bot.get_prefix(ctx.message)
            user_prefix = ''.join(user_prefixes) if user_prefixes else None
            embed = discord.Embed(title="globalchat command", description=f"This command can talk with other users globally\n```Syntax: {user_prefix}globalchat set <channel>\nExample: {user_prefix}globalchat set #general```")
            await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions(replied_user=False))
            return

async def setup(bot):
    await bot.add_cog(GlobalChat(bot))