import discord
from discord.ext import commands
import json
from datetime import datetime
import os

class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.data_folder = "Momo Data/MomoDM" 
        os.makedirs(self.data_folder, exist_ok=True)  # Crea la carpeta si no existe
        self.DM_file_path = os.path.join(self.data_folder, 'MomoDmMessages.json') 
        self.DM_file_path_channel_id = 1204357707210170378

    @commands.command(name="sdm", aliases=["Dm"])
    async def send_dm(self, ctx, user_id: int, *, message: str):
        # Encuentra al usuario por su ID
        user = self.bot.get_user(user_id)
        if user is None:
            await ctx.send("No se pudo encontrar al usuario.")
            return

        # Intenta enviar el DM
        try:
            await user.send(message)
            await ctx.send(f"Mensaje enviado a {user.name}")

            # Información para el embed y el archivo JSON
            data = {
                "sender_name": ctx.author.name,
                "sender_id": ctx.author.id,
                "recipient_name": user.name,
                "recipient_id": user.id,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
            # Enviar aviso en un canal concreto
            channel = self.bot.get_channel(self.DM_file_path_channel_id)   
            embed = discord.Embed(title="DM Enviado", color=discord.Color.blue())
            embed.add_field(name="De", value=f"{data['sender_name']} (ID: {data['sender_id']})", inline=False)
            embed.add_field(name="Para", value=f"{data['recipient_name']} (ID: {data['recipient_id']})", inline=False)
            embed.add_field(name="Mensaje", value=data['message'], inline=False)
            embed.add_field(name="Fecha", value=data['timestamp'], inline=False)
            await channel.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Error al enviar el mensaje: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        if not os.path.exists(self.DM_file_path):
            try:
                with open(self.DM_file_path, 'w') as f:
                    json.dump([], f) 
                voice_events_channel = self.bot.get_channel(self.DM_file_path_channel_id)
                if voice_events_channel:
                    embed = discord.Embed(
                        title="Archivo `MomoSendDm.json` creado y actualizado",
                        description="`MomoSendDm.json` almacena DM",
                        color=self.color_pastel
                    ) 
                await self.bot.get_channel(self.DM_file_path_channel_id).send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Error",
                    description=f"Error al crear el archivo `MomoSendDm.json`: ```{e}```",
                    color=self.color_pastel
                )
                await self.bot.get_channel(self.canal_error_id).send(embed=embed)

async def setup(bot):
    await bot.add_cog(DM(bot)) 