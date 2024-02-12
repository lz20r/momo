import os
import re
import json
import discord
from discord.ext import commands

class momochatEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.globalchat_dir = 'Momo Data/Momo Global Chat'
        self.globalchat_file = os.path.join(self.globalchat_dir, 'MomoGlobalchat.json')
        
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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return 
            
        global_chat_config = self.load_global_chat_config()
        message_channel_id = message.channel.id

        if message_channel_id in global_chat_config.values():
            author_name = message.author.name
            icon_author = message.author.avatar.url if message.author.avatar else discord.Embed.Empty
            server_name = message.guild.name
            server_icon = message.guild.icon.url if message.guild.icon else discord.Embed.Empty
            embed = discord.Embed(title=f"{self.bot.user.name} chat.")
            embed.set_author(name=author_name, icon_url=icon_author)
            embed.set_footer(text=f'message sent in {server_name}', icon_url=f'{server_icon}')
            embed.set_thumbnail(url=icon_author)

            links = re.findall(r'https?://[^\s]+', message.content)

            image_links = [link for link in links if re.search(r'\.(jpg|png|jpeg|gif)$', link)]

            if image_links:
                for image_link in image_links:
                    embed.set_image(url=image_link)
                    for channel_id in global_chat_config.values():
                        global_channel = self.bot.get_channel(channel_id)
                        if global_channel:
                            await global_channel.send(embed=embed)
            else:
                embed.description = f'content: {message.content}'
                for channel_id in global_chat_config.values():
                    global_channel = self.bot.get_channel(channel_id)
                    if global_channel:
                        await global_channel.send(embed=embed)
                await message.delete()

async def setup(bot):
    await bot.add_cog(momochatEvent(bot))