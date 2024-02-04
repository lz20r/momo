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
        self.canal_notificacion_id = 1202160434686201896   
        self.usuario_notificacion_id = 1143237780466569306   
        self.canal_error_id = 1202541792478887936
        self.color_pastel = 0xFFC0CB  

    @commands.Cog.listener()
    async def on_ready(self):     
        if not self.json_created:
            # Obtén el canal específico donde deseas enviar los mensajes de confirmación
            confirmation_channel_id = 1203112815255097474   
            confirmation_channel = self.bot.get_channel(confirmation_channel_id)  
            
        try:
            with open(self.json_file_path, 'r') as f:
                self.welcomed_guilds = json.load(f)
        except FileNotFoundError:
            self.messages_guilds = {}	
 
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignora los mensajes del bot para evitar bucles infinitos
        if message.author.bot:
            return  
        # Define los datos del mensaje
        mensaje = {
            "nombre_usuario": str(message.author),
            "nombre_servidor": str(message.guild),
            "mensaje_enviado": message.content,
            "canal": str(message.channel),
        }

        # Verifica si el usuario está en un canal de voz
        if isinstance(message.author, discord.Member) and message.author.voice:
            mensaje["canal_de_voz"] = str(message.author.voice.channel)

        # Verifica si el mensaje es repetido
        if await self.es_mensaje_repetido(mensaje):
            return

        # Agrega el nuevo mensaje al archivo JSON
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

        # Envía un Embed al canal de notificación
        embed = discord.Embed(
            title="New Message",
            color=self.color_pastel
        )
        embed.add_field(name="Server", value=message.guild.name)
        embed.add_field(name="Canal", value=message.channel.mention)
        embed.add_field(name="User", value=message.author.mention)
        embed.add_field(name="Message", value=message.content)

        # Verifica si el usuario está en un canal de voz y lo agrega al Embed
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

    async def es_mensaje_repetido(self, mensaje):
        # Ruta al archivo JSON en la carpeta "Cinnamon Messages"
        nombre_archivo = "MomoMessageMembers.json"
        ruta_archivo = os.path.join(self.data_folder, nombre_archivo)

        # Carga los datos existentes (si el archivo ya existe)
        try:
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, "r") as archivo:
                    datos = json.load(archivo)
                    for dato in datos:
                        # Verifica si el mensaje es repetido
                        if (dato["nombre_usuario"] == mensaje["nombre_usuario"] and
                            dato["mensaje_enviado"] == mensaje["mensaje_enviado"] and
                            dato.get("canal") == mensaje["canal"]):
                            return True   
        except Exception as e:
            embed = discord.Embed( 
                title="Error",
                description=f"Error al cargar el archivo JSON: ```{ruta_archivo}`",
                color=self.color_pastel
            )
            self.bot.get_channel(self.canal_error_id).send(embed=embed)
            return False

    async def agregar_mensaje(self, nuevo_mensaje):
        # Ruta al archivo JSON en la carpeta "Cinnamon Messages"
        nombre_archivo = "MomoMessageMembers.json"
        ruta_archivo = os.path.join(self.data_folder, nombre_archivo)

        # Carga los datos existentes (si el archivo ya existe)
        try:
            if os.path.exists(ruta_archivo): 
                with open(ruta_archivo, "r") as archivo:
                    datos = json.load(archivo)  
            else:
                datos = [] 
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error al cargar el archivo JSON: ```{e}```",
                color=self.color_pastel
            )
            self.bot.get_channel(self.canal_error_id).send(embed=embed)
            return False
        # Agrega el nuevo mensaje a la lista de mensajes
        datos.append(nuevo_mensaje)

        try:
            # Guarda los datos actualizados en el archivo JSON con indentación
            with open(ruta_archivo, "w") as archivo:
                json.dump(datos, archivo, indent=2)
                embed = discord.Embed(
                    title="Archivo `MomoMessageMembers`.js` creado",
                    description="El archivo JSON para almacenar los servidoresbienvenidos ha sido creado.", 
                    color=self.color_pastel
                )
                await self.bot.get_channel(self.canal_notificacion_id).send(embed=embed) 
            return True
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error al guardar el archivo JSON: ```{e}```",
                color=self.color_pastel
            )
            self.bot.get_channel(self.canal_error_id).send(embed=embed)
            return False

async def setup(bot):
    await bot.add_cog(MessageLogger(bot))
