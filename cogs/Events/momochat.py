from errno import EMEDIUMTYPE
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
                embed = discord.Embed(  
                    description="Please specify a channel to set for Momo Global Chat.\n"
                            f"```Momo Usage: {momousersprefix}mgchat set <channel>\n"
                            f"Momo Example: {momousersprefix}mgchat set #channel```"
                )
                await ctx.send(embed=embed)
                return

            self.globalchat[str(ctx.guild.id)] = channel.id
            self.savemomoglobalchat()
            embed = discord.Embed( 
                description=f"Successfully set {channel.mention} as the Momo Global Chat channel." 
            ) 
            await ctx.send(embed=embed)

        elif action == "remove":
            if str(ctx.guild.id) in self.globalchat:
                del self.globalchat[str(ctx.guild.id)]
                self.savemomoglobalchat()
                embed = discord.Embed( 
                    description=f"Successfully removed {channel.mention} as the Momo Global Chat channel." 
                )    
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(  
                    description="Momo Global Chat is not configured yet try again\n"
                            f"```Momo Usage: {momousersprefix}mgchat set <channel>\n"
                            f"Momo Example: {momousersprefix}mgchat set #channel```"
                )
                await ctx.send(embed = embed)

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
        # Ignorar mensajes de bots y asegurarse de que el mensaje proviene de un canal de texto
        if message.author.bot or not isinstance(message.channel, discord.TextChannel):
            return

        momoauthorname = message.author.name
        momoauthoricon = message.author.avatar.url if message.author.avatar else discord.Embed.Empty
        momoservername = message.guild.name
        momoservericon = message.guild.icon.url if message.guild.icon else discord.Embed.Empty
        momomessage = message.content  # Asegúrate de usar .content para obtener el texto del mensaje
        momochannel = message.channel
        momoguildid = message.guild.id

        if str(momoguildid) in self.globalchat and message.channel.id == self.globalchat[str(momoguildid)]:
            # Construir el mensaje y el embed
            message_content = f"<:momostarw:1206266007090364486> Message: {momomessage}"
            embed = discord.Embed(description=message_content, color=self.color_pastel)
            embed.set_author(name=momoauthorname, icon_url=momoauthoricon)
            embed.set_footer(text=f"{momoservername}", icon_url=momoservericon)
            embed.set_thumbnail(url=momoauthoricon)

            # Eliminar el mensaje original para evitar duplicaciones
            await message.delete()

            # Enviar el embed a todos los canales configurados, excepto al de origen
            for guild_id, channel_id in self.globalchat.items():
                if guild_id != str(momoguildid):
                    target_channel = self.bot.get_channel(int(channel_id))
                    if target_channel:
                        # Enviar el embed creado al canal objetivo
                        await target_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GlobalChat(bot))
