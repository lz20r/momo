import os
import json
import discord
from discord.ext import commands

class MessageLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = "Momo Data"
        os.makedirs(self.data_folder, exist_ok=True)
        self.json_file_path = os.path.join(self.data_folder, 'MomoMessageMembers.json')
        self.logging_enabled = True  # Bandera para habilitar/deshabilitar los logs
        self.voice_events_path = os.path.join(self.data_folder, 'MomoVoiceEvents.json') 
        self.voice_events_channel_id = 1203834523352047656
        self.canal_json_id = 1203112815255097474
        self.canal_notificacion_id = 1202160434686201896
        self.usuario_notificacion_id = 1143237780466569306
        self.canal_error_id = 1202541792478887936
        self.color_pastel = 0xFFC0CB

    @commands.Cog.listener()
    async def on_ready(self):
        if not os.path.exists(self.json_file_path):
            try:
                with open(self.json_file_path, 'w') as f:
                    json.dump([], f)
                voice_events_channel = self.bot.get_channel(self.voice_events_channel_id)
                if voice_events_channel:
                    embed = discord.Embed(
                        title="Archivo `MomoMessageMembers.json` creado y actualizado",
                        description="El archivo `MomoMessageMembers.json` se utiliza para almacenar los mensajes enviados, editados y eliminados por los usuarios.",
                        color=self.color_pastel
                    )
                    await voice_events_channel.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Error",
                    description=f"Error al crear el archivo `MomoMessageMembers.json`: ```{e}```",
                    color=self.color_pastel
                )
                await self.bot.get_channel(self.canal_error_id).send(embed=embed)

        if not os.path.exists(self.voice_events_path):
            try:
                with open(self.voice_events_path, 'w') as f:
                    json.dump([], f)
                voice_events_channel = self.bot.get_channel(self.voice_events_channel_id)
                if voice_events_channel:
                    embed = discord.Embed(
                        title="Archivo `MomoVoiceEvents.json` creado y actualizado",
                        description="El archivo `MomoVoiceEvents.json` se utiliza para almacenar los eventos de entrada y salida de los usuarios en los canales de voz.",
                        color=self.color_pastel
                    )
                    await voice_events_channel.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Error",
                    description=f"Error al crear el archivo `MomoVoiceEvents.json`: ```{e}```",
                    color=self.color_pastel
                )
                await self.bot.get_channel(self.canal_error_id).send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not self.logging_enabled:
            return

        if isinstance(message.channel, discord.TextChannel) and not message.channel.permissions_for(message.guild.me).read_messages:
            return

        mensaje = {
            "nombre_usuario": str(message.author),
            "nombre_servidor": str(message.guild),
            "accion": "enviado",
            "mensaje": message.content,
            "canal": str(message.channel),
            "timestamp": str(message.created_at)
        }

        if isinstance(message.author, discord.Member) and message.author.voice:
            mensaje["canal_de_voz"] = str(message.author.voice.channel)

        await self.agregar_mensaje(mensaje)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not self.logging_enabled:
            return
        mensaje = {
            "nombre_usuario": str(message.author),
            "nombre_servidor": str(message.guild),
            "accion": "eliminado",
            "mensaje": message.content,
            "canal": str(message.channel),
            "timestamp": str(message.created_at)
        }
        await self.agregar_mensaje(mensaje)
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or after.author.bot or not self.logging_enabled:
            return
        mensaje = {
            "nombre_usuario": str(after.author),
            "nombre_servidor": str(after.guild),
            "accion": "editado",
            "mensaje_anterior": before.content,
            "mensaje_nuevo": after.content,
            "canal": str(after.channel),
            "timestamp": str(after.created_at)
        }
        await self.agregar_mensaje(mensaje)
        
    @commands.Cog.listener()
    async def agregar_mensaje(self, mensaje):
        try:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, "r") as archivo:
                    datos = json.load(archivo)
            else:
                datos = []
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error al cargar el archivo 'MomoMessageMembers.json': ```{e}```",
                color=self.color_pastel
            )
            self.bot.get_channel(self.canal_error_id).send(embed=embed)
            return False

        datos.append(mensaje)

        try:
            with open(self.json_file_path, "w") as archivo:
                json.dump(datos, archivo, indent=4)
            return True
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error al guardar el archivo `MomoMessageMembers.json`: ```{e}```",
                color=self.color_pastel
            )
            await self.bot.get_channel(self.canal_error_id).send(embed=embed)
            return False

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            if before.channel:
                await self.registrar_evento(f"{member} salió del canal de voz {before.channel.name}.")
            if after.channel:
                await self.registrar_evento(f"{member} entró al canal de voz {after.channel.name}.")

    @commands.Cog.listener()
    async def registrar_evento(self, evento):
        try:
            evento_data = {
                "evento": evento,
                "timestamp": str(discord.utils.utcnow())
            }
            if os.path.exists(self.voice_events_path):
                with open(self.voice_events_path, "r") as archivo:
                    registros = json.load(archivo)
            else:
                registros = []
            registros.append(evento_data)
            with open(self.voice_events_path, "w") as archivo:
                json.dump(registros, archivo, indent=4)
            canal_notificacion = self.bot.get_channel(self.canal_notificacion_id)
            if canal_notificacion:
                embed = discord.Embed(
                    title="Voice Event",
                    description=evento,
                    color=self.color_pastel
                )
                await canal_notificacion.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error al registrar evento: ```{e}```",
                color=self.color_pastel
            )
            await self.bot.get_channel(self.canal_error_id).send(embed=embed)

async def setup(bot):
    await bot.add_cog(MessageLogger(bot))
