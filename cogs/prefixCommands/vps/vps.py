
import os
import json
import asyncio
import discord
from discord.ext import commands

from cogs.prefixCommands.setup.setPrefix import Prefix

class host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None  

        # Define la ruta del archivo JSON dentro de la carpeta "Momo Data"
        self.data_folder = "Momo Data"
        os.makedirs(self.data_folder, exist_ok=True)  # Crea la carpeta si no existe
        self.config_file_path = os.path.join(self.data_folder, 'MomoInfoHost.json')        

        # Cargar la configuración desde el archivo
        self.load_config()

    def load_config(self):
        try:
            # Abre el archivo de configuración desde la carpeta "Momo Data"
            with open(self.config_file_path, "r") as file:
                config = json.load(file)
                self.channel_id = config.get("channel_id")
        except FileNotFoundError:
            # Si el archivo no existe, se crea uno nuevo
            self.save_config()

    def save_config(self):
        # Guarda la configuración en el archivo dentro de la carpeta "Momo Data"
        config = {"channel_id": self.channel_id}
        with open(self.config_file_path, "w") as file:
            json.dump(config, file, indent=4)

    async def request_info(self, ctx):
        """Solicita la información necesaria para rellenar las plantillas."""
        info = {}  # Diccionario para almacenar la información solicitada
        prompts = ["Mail", "Username", "First Name", "Last Name", "Password", "Name Server", "CPU", "RAM", "Disco", "Egg"]  # Prompts para solicitar la información 
        for prompt in prompts:
            embed = discord.Embed(description=f"<:mtflechaheart:1203068677570830407> {ctx.author.mention} write your {prompt}: ")
            await ctx.send(embed=embed)
            try:  
                # Espera la respuesta del usuario durante 60 segundos
                response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
                info[prompt] = response.content 
            except asyncio.TimeoutError:
                embed = discord.Embed(description="The time proporcionate end up, try again")
                await ctx.send(embed=embed, delete_after=10)
                return None
        # Retorna el diccionario con la información
        return info

    @commands.command(name="setuphost", aliases=["hCh"])
    @commands.has_permissions(administrator=True)
    async def setup_hostchannel(self, ctx, channel: discord.TextChannel):
        """Configura el canal donde se enviarán las plantillas rellenadas."""
        self.channel_id = channel.id
        self.save_config()  # Guardar la configuración en el archivo
        embed = discord.Embed(description=f"Canal configurado correctamente como {channel.mention} para enviar las plantillas rellenadas.")
        await ctx.send(embed=embed)
        
    @commands.command(name="request_hostInfo", aliases=["rHostI"])
    async def request_host_info(self, ctx):
        """Solicita la información necesaria para rellenar las plantillas."""
        if self.channel_id is None:
            embed = discord.Embed(description="El canal de destino no está configurado. Usa el comando `setuphost` para configurarlo.")
            await ctx.send(embed=embed, delete_after=10)
            return
        infromation = discord.Embed(description=f"Please, help {self.bot.user.name} to recollect the following information and then you will be able to having your server as soon as possible:") 
        await ctx.send(embed=infromation)        
        info = await self.request_info(ctx)  # Solicitar información al usuario
        embed = discord.Embed(description=f"{ctx.author.mention} tysm for collaborating with us using {self.bot.user.name}, now we can process this info to the administrator and we will be able to having your server and it will be as soon as possible.")
        await ctx.send(embed=embed)
        if info: 
            await self.send_host_template(ctx, info)  # Enviar la plantilla con la información proporcionada
  
 
    @commands.command(name="edit_hostInfo", aliases=["eHostI"])
    async def edit_host_info(self, ctx):
        """Muestra la información actual de cada campo y permite su edición si así se desea."""
        valid_fields = ["mail", "username", "first name", "last name", "password", "name server", "cpu", "ram", "disco", "egg"]
        info = await self.request_info(ctx)  # Suponemos que esta función recupera la info actual

        for field in valid_fields:
            # Muestra la información actual del campo
            current_value = info.get(field.title(), "No disponible")  # Asume que `info` es un diccionario con la información actual
            await ctx.send(f"El valor actual para '{field}' es: {current_value}. ¿Quieres cambiarlo? Responde con 'si' para confirmar o 'no' para continuar.")

            try:
                decision = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["si", "no"], timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send("Se agotó el tiempo de espera. Pasando al siguiente campo.")
                continue

            if decision.content.lower() == "si":
                await ctx.send(f"Introduce el nuevo valor para '{field}':")

                try:
                    new_value_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60.0)
                    new_value = new_value_msg.content
                    # Actualiza el campo con el nuevo valor
                    info[field.title()] = new_value
                    await ctx.send(f"Campo '{field}' actualizado a: {new_value}")
                except asyncio.TimeoutError:
                    await ctx.send("Se agotó el tiempo de espera para el nuevo valor. Pasando al siguiente campo.")
                    continue
            else:
                await ctx.send(f"Manteniendo el valor actual para '{field}'.")

        # Aquí puedes enviar la información actualizada donde sea necesario, por ejemplo:
        await self.send_host_template(ctx, info)
        await ctx.send("Revisión completa. Todos los cambios solicitados han sido aplicados.")


            
    async def send_host_template(self, ctx, info):
        """Envía la plantilla con la información proporcionada al canal designado."""
        if self.channel_id is None:
            embed = discord.Embed(description="El canal de destino no está configurado. Usa el comando `setuphost` para configurarlo.")
            await ctx.send(embed=embed, delete_after=10)
            return

        # Crear la plantilla utilizando la información proporcionada por el usuario
        template = f"""
# INFORMATION NECESSARY FOR HOSTING A SERVER
## **{ctx.author.mention} -- {ctx.author.id}**
- **{ctx.author.mention} Credentials:**
- Mail: {info.get("Mail")}
- Username: {info.get("Username")}
- First Name: {info.get("First Name")}
- Last Name: {info.get("Last Name")}
- Password: {info.get("Password")}
————-————-————-————-————
- **Core Details**   
            - Server Name: {info.get("Name Server")}
- **Allocation Management** 
- CPU: {info.get("CPU")}
- RAM: {info.get("RAM")}
- Disk: {info.get("Disco")}
- **Node**
            - Egg (Lenguaje que usa tu bot): {info.get("Egg")}
"""

        canal_destino = ctx.guild.get_channel(self.channel_id)
        if canal_destino:
            message = await canal_destino.send(template)
            embed = discord.Embed(description=f"Plantilla enviada correctamente a {canal_destino.mention}.")
            await ctx.send(embed=embed)
            
            await message.add_reaction('✏️')
            await message.add_reaction('✔️')
            await message.add_reaction('❌')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['✏️', '✔️', '❌'] and reaction.message.id == message.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check)
                if str(reaction.emoji) == '✔️':
                    embed = discord.Embed(description="Información confirmada.")
                    await message.edit(embed=embed, delete_after=10) 
                elif str(reaction.emoji) == '✏️':
                    embed = discord.Embed(description="Edición solicitada. Por favor, use el comando edit_hostInfo para editar.")
                    ctx.send(embed=embed, delete_after=10)
                elif str(reaction.emoji) == '❌':
                    await message.clear_reactions()  # Elimina todas las reacciones
                    embed = discord.Embed(description="Información rechazada y reacciones eliminadas.")
                    await message.edit(embed=embed, delete_after=10)                 
                
            except asyncio.TimeoutError:
                embed = discord.Embed(description="No se recibieron reacciones en el tiempo establecido.")
                await message.edit(embed=embed, delete_after=10) 
async def setup(bot):
    await bot.add_cog(host(bot)) 
