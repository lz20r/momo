import discord
from discord.ext import commands
import json
import os

class DMNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = "Momo Data/MomoDM" 
        self.data_file = "MomoDmUsers.json"
      
        # Asegúrate de que la carpeta existe
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel) and message.author != self.bot.user:
            # Construye la ruta completa al archivo
            file_path = os.path.join(self.data_folder, self.data_file)

            # Lee el archivo existente o crea uno nuevo si no existe
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    data = json.load(file)
            else:
                data = {}

            # Usa el ID del usuario como clave para organizar los chats por usuario
            user_id = str(message.author.id)
            if user_id not in data:
                data[user_id] = {
                    "name": message.author.name,
                    "messages": []
                }

            # Añade el nuevo mensaje al registro del usuario
            data[user_id]["messages"].append({
                "sender": message.author.name,
                "content": message.content
            })

            # Guarda los datos actualizados en el archivo JSON
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

            # Envía una notificación a un canal específico
            # Reemplaza 'id_del_canal' con el ID real del canal de Discord
            channel = self.bot.get_channel(1204094912145002596)
            if channel:
                await channel.send(f"Recibí un DM de {message.author.name} (ID: {message.author.id})")

async def setup(bot):
    await bot.add_cog(DMNotification(bot)
