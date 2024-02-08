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
        self.voice_events_path = os.path.join(self.data_folder, 'MomoVoiceEvents.json') 
        self.voice_events_channel_id = 1203834523352047656
        self.canal_json_id = 1203112815255097474
        self.canal_notificacion_id = 1202160434686201896
        self.usuario_notificacion_id = 1143237780466569306
        self.canal_error_id = 1202541792478887936
        self.color_pastel = 0xFFC0CB

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.json_created:
            confirmation_channel_id = 1203112815255097474
            confirmation_channel = self.bot.get_channel(confirmation_channel_id)
        try:
            with open(self.json_file_path, 'r') as f:
                self.welcomed_guilds = json.load(f)
        except FileNotFoundError:
            self.messages_guilds = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        mensaje = {
            "nombre_usuario": str(message.author),
            "nombre_servidor": str(message.guild),
            "mensaje_enviado": message.content,
            "canal": str(message.channel),
        }

        if isinstance(message.author, discord.Member) and message.author.voice:
            mensaje["canal_de_voz"] = str(message.author.voice.channel)

        if await self.es_mensaje_repetido(mensaje):
            return

        if not await self.agregar_mensaje(mensaje):
            canal_notificacion = self.bot.get_channel(self.canal_notificacion_id)
            if canal_notificacion:
                await canal_notificacion.send(f"Error: No se pudo crear o actualizar el archivo `{self.json_file_path}` en la carpeta `{self.data_folder}`.")
                usuario_notificacion = self.bot.get_user(self.usuario_notificacion_id)
                if usuario_notificacion:
                    await canal_notificacion.send(f"{usuario_notificacion.mention}, ocurrió un error al guardar el archivo JSON.")
                else:
                    print("No se pudo encontrar al usuario para la notificación. Asegúrate de que el ID del usuario sea correcto.")
            else:
                print("No se pudo encontrar el canal de notificación. Asegúrate de que el ID del canal sea correcto.")

        embed = discord.Embed(
            title="New Message",
            color=self.color_pastel
        )
        embed.add_field(name="Server", value=message.guild.name)
        embed.add_field(name="Canal", value=message.channel.mention)
        embed.add_field(name="User", value=message.author.mention)
        embed.add_field(name="Message", value=message.content)

        if isinstance(message.author, discord.Member) and message.author.voice:
            embed.add_field(name="Voice Channel", value=message.author.voice.channel.name, inline=False)

        canal_notificacion = self.bot.get_channel(self.canal_notificacion_id)
        if canal_notificacion:
            await canal_notificacion.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description=f"warning: Could not find the channel for notifications. Make sure the channel ID is correct.",
                color=self.color_pastel
            )
            self.bot.get_channel(self.canal_error_id).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        await self.eliminar_mensaje(message.id)
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or after.author.bot:
            return
        await self.actualizar_mensaje(before.id, after.content)
    @commands.Cog.listener()
    async def es_mensaje_repetido(self, mensaje):
        try:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, "r") as archivo:
                    datos = json.load(archivo)
                    for dato in datos:
                        if (dato["nombre_usuario"] == mensaje["nombre_usuario"] and
                            dato["mensaje_enviado"] == mensaje["mensaje_enviado"] and
                            dato.get("canal") == mensaje["canal"]):
                            return True
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error al cargar el archivo 'MomoMessageMembers.json': ```{e}```",
                color=self.color_pastel
            )
            self.bot.get_channel(self.canal_error_id).send(embed=embed)
            return False
    @commands.Cog.listener()
    async def agregar_mensaje(self, nuevo_mensaje):
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

        datos.append(nuevo_mensaje)

        try:
            with open(self.json_file_path, "w") as archivo:
                json.dump(datos, archivo, indent=4)
                embed = discord.Embed(
                    title="Archivo `MomoMessageMembers.json`",
                    description="Se ha actualizado",
                    color=self.color_pastel
                )
                await self.bot.get_channel(self.canal_json_id).send(embed=embed)
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
    async def eliminar_mensaje(self, mensaje_id):
        try:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, "r") as archivo:
                    datos = json.load(archivo)
                    datos = [dato for dato in datos if dato.get("mensaje_id") != mensaje_id]
                with open(self.json_file_path, "w") as archivo:
                    json.dump(datos, archivo, indent=4)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error al eliminar el mensaje del archivo `MomoMessageMembers.json`: ```{e}```",
                color=self.color_pastel
            )
            await self.bot.get_channel(self.canal_error_id).send(embed=embed)
    @commands.Cog.listener()
    async def actualizar_mensaje(self, mensaje_id, nuevo_contenido):
        try:
            if os.exists(self.json_file_path):
                with open(self.json_file_path, "r") as archivo:
                    datos = json.load(archivo)
                    for dato in datos:
                        if dato.get("mensaje_id") == mensaje_id:
                            dato["mensaje_enviado"] = nuevo_contenido
                            break
                with open(self.json_file_path, "w") as archivo:
                    json.dump(datos, archivo, indent=4)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error al actualizar el mensaje en el archivo `MomoMessageMembers.json`: ```{e}```",
                color=self.color_pastel
            )
            await self.bot.get_channel(self.canal_error_id).send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            if before.channel:
                await self.registrar_evento(f"{member} salió del canal de voz {before.channel.name}.")
            if after.channel:
                await self.registrar_evento(f"{member} entró al canal de voz {after.channel.name}.")

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

    @commands.Cog.listener()
    async def on_ready(self):
        if not os.path.exists(self.voice_events_path):
            try:
                with open(self.voice_events_path, 'w') as f:
                    json.dump([], f) 
                voice_events_channel = self.bot.get_channel(self.voice_events_channel_id)
                if voice_events_channel:
                    embed = discord.Embed(
                        title="Archivo `MomoMeVoiceEventsssageMembers.json` creado y actualizado",
                        description="`MomoVoiceEvents.json` almacena los mensajes enviados por cualquier usuario en cualquier servidor que tenga a Momo",
                        color=self.color_pastel
                    ) 
                await self.bot.get_channel(self.voice_events_channel_id).send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title=f"Error in `MomoMeVoiceEventsssageMembers.json`",
                    description=f"Error al crear el archivo: ```{e}```",
                    color=self.color_pastel
                )
                await self.bot.get_channel(self.canal_error_id).send(embed=embed)

async def setup(bot):
    await bot.add_cog(MessageLogger(bot))
