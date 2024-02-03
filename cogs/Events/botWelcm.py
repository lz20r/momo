import os
import json
import discord
from discord.ext import commands

class BotWelcm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.data_folder = "Momo Data"  # Carpeta donde se almacenarán los archivos JSON
        os.makedirs(self.data_folder, exist_ok=True)  # Crea la carpeta si no existe
        self.json_file_path = os.path.join(self.data_folder, 'WelcomeGuildsMomoDm.json')
        self.color_pastel = 0xFFC0CB 
        self.json_created = False 

        try: 
            with open(self.json_file_path, 'r') as f:
                self.welcomed_guilds = json.load(f)
        except FileNotFoundError:
            self.welcomed_guilds = {}

    @commands.Cog.listener()
    async def on_ready(self): 
            if not os.path.exits(self.json_file_path): 
                confirmation_channel_id = 1203112815255097474  # Reemplaza con la ID de tu canal
                confirmation_channel = self.bot.get_channel(confirmation_channel_id)

                # Crea el archivo JSON si no existe y lo escribe
                with open(self.json_file_path, 'w') as f: 
                    json.dump({}, f, indent=4)
                    embed = discord.Embed(title="Archivo `WelcomeGuildsMomoDm.json` creado", description="Archivo para almacenar los los mensajes de bienvenidos por Momo ha sido creado.", color=self.color_pastel)
                    await confirmation_channel.send(embed=embed)
    @commands.Cog.listener() 
    async def on_guild_join(self, guild): 
        welcome_message = f"""
        ¡Muchas gracias por añadirme a tu servidor {guild.name}! 

        Espero cumplir con tus expectativas y ayudarte en tu servidor. Aquí tienes algunas instrucciones para empezar:
        > <:Flechaheart:1203068677570830407> Mi prefijo por defecto es `m.`.
        > <:Flechaheart:1203068677570830407> Puedes ver todos mis comandos con `m.help`.
        > <:Flechaheart:1203068677570830407> Puedes configurarme a través de mi Dashboard: [Enlace a Dashboard](https://cinammon.es/dashboard).
        > <:Flechaheart:1203068677570830407> Puedes acceder a mi Host: [Enlace a Dashboard](https://cinammon.es/panel). 
        > <:Flechaheart:1203068677570830407> ¿Te interesa potenciar tu experiencia y apoyarme? ¡Puedes hacerlo a través de mi Patreon! [Enlace a Patreon](https://www.patreon.com/cinammon)
        > <:Flechaheart:1203068677570830407> Si necesitas una guía, tengo una muy completa: [Guía](https://docs.cinammon.es)
        > <:Flechaheart:1203068677570830407> ¿Necesitas ayuda? Puedes unirte a mi servidor de soporte: [Servidor de Soporte](https://discord.gg/mintandcinammon).
        """ 
        announcement_channel = None

        # Buscar un canal de anuncios en el servidor
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages and "anuncio" in channel.name.lower():
                announcement_channel = channel
                break

        if announcement_channel:
            # Si se encuentra un canal de anuncios, enviar el mensaje en formato de embed
            embed = discord.Embed(title=f"Bienvenido a {guild.name}!", description=welcome_message, color=self.color_pastel)
            await announcement_channel.send(embed=embed)
        else:
            # Si no se encuentra un canal de anuncios, enviar el mensaje al primer canal de texto que encuentre en formato de embed
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    embed = discord.Embed(title=f"Bienvenido a {guild.name}!", description=welcome_message, color=self.color_pastel)
                    await channel.send(embed=embed)
                    break

        if guild.id in self.welcomed_guilds:
            # Si la ID del servidor ya está presente en el archivo JSON, enviar un mensaje de advertencia en formato de embed
            confirmation_channel_id = 1203112920934785084  # Reemplaza con la ID de tu canal de advertencia
            confirmation_channel = self.bot.get_channel(confirmation_channel_id)
            
            if confirmation_channel:
                embed = discord.Embed(title="¡Advertencia!", description=f"La ID del servidor {guild.id} ya estaba presente `WelcomeGuildsMomoDm.json`.", color=self.color_pastel)
                await confirmation_channel.send(embed=embed)

        # Otorgar al bot el rol más alto en el servidor
        try:
            highest_role = guild.roles[-1]
            await self.bot.user.add_roles(highest_role)
        except Exception as e:
            print(f"Error al otorgar el rol más alto al bot: {e}")

        self.welcomed_guilds[guild.id] = guild.name
        self.save_welcomed_guilds_to_json()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if guild.id in self.welcomed_guilds:
            del self.welcomed_guilds[guild.id]  
            self.save_welcomed_guilds_to_json() 
 
    def save_welcomed_guilds_to_json(self):
        with open(self.json_file_path, 'w') as f:
            json.dump(self.welcomed_guilds, f, indent=4)   

async def setup(bot):  
    await bot.add_cog(BotWelcm(bot)) 
