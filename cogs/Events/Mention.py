import discord
from discord.ext import commands
import os 

class MentionCog(commands.Cog):
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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(self.bot.user.mention):
            prefix = await self.bot.get_prefix(message)
            embed_hello = discord.Embed(title="", description=f"<:mtinfo1:1205311004066451507> my prefix here is `{prefix}`")
            await message.reply(embed=embed_hello)

        global_chat_config = self.load_global_chat_config()
        message_channel_id = message.channel.id

        if message_channel_id in global_chat_config.values():
            author_name = message.author.name
            icon_author = message.author.avatar.url if message.author.avatar else discord.Embed.Empty
            server_name = message.guild.name
            server_icon = message.guild.icon.url if message.guild.icon else discord.Embed.Empty
            embed = discord.Embed(title="launted chat")
            embed.set_author(name=author_name, icon_url=icon_author)
            embed.set_footer(text=f'{server_name}', icon_url=f'{server_icon}')

            links = re.findall(r'https?://[^\s]+', message.content)

            image_links = [link for link in links if re.search(r'\.(jpg|png|jpeg|gif)$', link)]

            if image_links:
                for image_link in image_links:
                    embed.set_image(url=image_link)
                    for channel_id in global_chat_config.values():
                        global_channel = self.client.get_channel(channel_id)
                        if global_channel:
                            await global_channel.send(embed=embed)
            else:
                embed.description = f'Content: {message.content}'
                for channel_id in global_chat_config.values():
                    global_channel = self.client.get_channel(channel_id)
                    if global_channel:
                        await global_channel.send(embed=embed)
                await message.delete()

async def setup(bot):
    await bot.add_cog(MentionCog(bot))