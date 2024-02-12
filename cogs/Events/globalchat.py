import http
import os
import json
import discord
from discord.ext import commands

class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = "Momo Data/Momo chat global"
        os.makedirs(self.data_folder, exist_ok=True)
        self.file_path = os.path.join(self.data_folder, 'MomoGlobalchat.json')
        self.color_pastel = 0xFFC0CB
        self.globalchat = self.loadmomoglobalchat()

    def loadmomoglobalchat(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        else:
            return {}
        
    def savemomoglobalchat(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.globalchat, f, indent=4)

    @commands.command(name='momochat', aliases=['mgchat'])
    async def momoglobalchat(self, ctx, action=None, *, channel: discord.TextChannel = None):
        momousersprefix = await self.bot.get_prefix(ctx.message)
        if isinstance(momousersprefix, list):
            momousersprefix = momousersprefix[0]

        if action is None:
            embed = discord.Embed(
                title="Momo Global Chat",
                description=f"Momo chat can join others users from other servers to talk with each other. Here's how to use it:\n"
                            f"```Momo Usage: {momousersprefix}mgchat set <channel>\n"
                            f"Momo Example: {momousersprefix}mgchat set #channel```",
                color=self.color_pastel
            )
            embed.set_footer(text="Momo Global Chat")   
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
            return

        if action == "set":
            if channel is None:
                await ctx.send("Please specify a channel to set for Momo Global Chat.")
                return

            self.globalchat[str(ctx.guild.id)] = channel.id
            self.savemomoglobalchat()
            await ctx.send(f"Successfully set {channel.mention} as the Momo Global Chat channel.")

        elif action == "remove":
            if str(ctx.guild.id) in self.globalchat:
                del self.globalchat[str(ctx.guild.id)]
                self.savemomoglobalchat()
                await ctx.send("Momo Global Chat channel removed successfully.")
            else:
                await ctx.send("Momo Global Chat is not configured for this server.")

        else:
            embed = discord.Embed(
                title="Momo Global Chat",
                 description=f"Invalid action. Here's how to use it:\n"
                            f"```Momo Usage: {momousersprefix}mgchat set <channel>\n"
                            f"Momo Example: {momousersprefix}mgchat remove <channel>```",
                color=self.color_pastel 
            )
            await ctx.send(embed=embed)
            
            
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignorar mensajes del propio bot o mensajes que no sean de canales de texto.
        if message.author.bot or not isinstance(message.channel, discord.TextChannel):
            return

        # Verificar si el canal del mensaje está en el chat global.
        if str(message.guild.id) in self.globalchat and message.channel.id == self.globalchat[str(message.guild.id)]:
            # Preparar el registro del mensaje para enviarlo a otros canales.
            embed = discord.Embed(description=message.content, color=self.color_pastel)
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
            embed.set_footer(text=f"Server: {message.guild.name}")
            

            # Recorrer todos los canales configurados en el chat global y enviar el mensaje.
            for guild_id, channel_id in self.globalchat.items():
                # Evitar enviar el mensaje al mismo canal de origen.
                if guild_id != str(message.guild.id):
                    target_channel = self.bot.get_channel(int(channel_id))
                    if target_channel:
                        await target_channel.send(embed=embed)
                            
async def setup(bot):
    await bot.add_cog(GlobalChat(bot))
