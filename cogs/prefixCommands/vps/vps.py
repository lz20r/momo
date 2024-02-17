import discord
from discord.ext import commands
import asyncio
import json
import os

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
            await ctx.send(f"Please, fill {prompt}:")
            try:
                # Espera la respuesta del usuario durante 60 segundos
                response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
                info[prompt] = response.content
            except asyncio.TimeoutError:
                await ctx.send("The time proporcionate end up, try again")
                return None
        # Retorna el diccionario con la información
        return info

    @commands.command(name="setuphost", aliases=["hCh"])
    @commands.has_permissions(administrator=True)
    async def setup_hostchannel(self, ctx, channel: discord.TextChannel):
        """Configura el canal donde se enviarán las plantillas rellenadas."""
        self.channel_id = channel.id
        self.save_config()  # Guardar la configuración en el archivo
        await ctx.send(f"Canal configurado correctamente como {channel.mention} para enviar las plantillas rellenadas.")
        
    @commands.command(name="request_hostInfo", aliases=["rHostI"])
    async def request_host_info(self, ctx):
        """Solicita la información necesaria para rellenar las plantillas."""
        if self.channel_id is None:
            await ctx.send("El canal de destino no está configurado. Usa el comando `setuphost` para configurarlo.")
            return
        info = await self.request_info(ctx)  # Solicitar información al usuario
        if info:
            await self.send_host_template(ctx, info)  # Enviar la plantilla con la información proporcionada

    @commands.command(name="edit_hostInfo", aliases=["eHostI"])
    @commands.has_permissions(administrator=True)
    async def edit_host_info(self, ctx, field: str, *, new_value: str):
        """Permite a los administradores editar la información."""
        if field.lower() in ["mail", "username", "first name", "last name", "password", "name server", "cpu", "ram", "disco", "egg"]:
            await ctx.send(f"Editando {field}...")
            info = await self.request_info(ctx)
            if info:
                info[field.title()] = new_value
                await self.send_host_template(ctx, info)
        else:
            await ctx.send("Campo inválido. Los campos válidos son: Mail, Username, First Name, Last Name, Password, Name Server, CPU, RAM, Disco, Egg.")
    async def send_host_template(self, ctx, info):
        """Envía la plantilla con la información proporcionada al canal designado."""
        if self.channel_id is None:
            await ctx.send("El canal de destino no está configurado. Usa el comando `setuphost` para configurarlo.")
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

        # Obtener el canal de destino
        canal_destino = ctx.guild.get_channel(self.channel_id)
        target_thread = discord.utils.get(ctx.guild.threads, id=self.thread_id)

        # Verificar si el hilo de destino existe
        

        # Verificar si el canal de destino existe
        if canal_destino and target_thread:
            # Enviar la plantilla al canal de destino
            message = await canal_destino.send(template) and await target_thread.send(template) 
            
            # Preguntar si se desean realizar cambios
            await message.add_reaction('✏️')
            try:
                if ctx.author.guild_permissions.administrator:
                    await message.add_reaction('✅')
                    await message.add_reaction('❌') 
                    
                # Esperar a que el usuario responda
                # Espera la respuesta del usuario durante 60 segundos
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in ['✅', '❌'])
                except asyncio.TimeoutError:
                    await ctx.send("No se recibieron cambios.")
                    return
                
                if str(reaction.emoji) == '✅':
                    await ctx.send("Plantilla rellenada correctamente.")
                elif str(reaction.emoji) == '❌':
                    await ctx.send("Plantilla no rellenada.")
                    return
            except asyncio.TimeoutError:
                await ctx.send("No se recibieron cambios.")
                return 

            # Verificar si el usuario es administrador y permitir la edición
            if ctx.author.guild_permissions.administrator:
                await ctx.send("Por favor, indica qué campo deseas editar (por ejemplo, `Mail`), seguido del nuevo valor:")
                try:
                    response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
                    parts = response.content.split(maxsplit=1)
                    if len(parts) == 2:
                        field_to_edit = parts[0]
                        new_value = parts[1]
                        # Actualizar el mensaje con el nuevo valor
                        edited_template = template.replace(f"{field_to_edit}: {info.get(field_to_edit)}", f"{field_to_edit}: {new_value}")
                        await message.edit(content=edited_template)
                        await ctx.send(f"El campo `{field_to_edit}` ha sido editado correctamente.")
                    else:
                        await ctx.send("Formato incorrecto. Por favor, indica el campo seguido del nuevo valor.")
                except asyncio.TimeoutError:
                    await ctx.send("El tiempo proporcionado ha terminado, no se realizaron cambios.")
            else:
                await ctx.send("Solo los administradores pueden editar los campos.")
        else:
            await ctx.send("No se encontró el canal de destino.")

async def setup(bot):
    await bot.add_cog(host(bot))
