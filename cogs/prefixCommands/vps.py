import discord
from discord.ext import commands
import asyncio
import json
import os

class VPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None  

        # Define la ruta del archivo JSON dentro de la carpeta "Momo Data"
        self.data_folder = "Momo Data"
        os.makedirs(self.data_folder, exist_ok=True)  # Crea la carpeta si no existe
        self.config_file_path = os.path.join(self.data_folder, 'MomoInfoVPS.json')        

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

    @commands.command(name="setupVPS", aliases=["vCh"])
    async def setup_vpschannel(self, ctx, channel: discord.TextChannel):
        """Configura el canal donde se enviarán las plantillas rellenadas."""
        self.channel_id = channel.id
        self.save_config()  # Guardar la configuración en el archivo
        await ctx.send(f"Canal configurado correctamente como {channel.mention} para enviar las plantillas rellenadas.")
        
    @commands.command(name="request_vpsInfo", aliases=["rVpsI"])
    async def request_vps_info(self, ctx):
        """Solicita la información necesaria para rellenar las plantillas."""
        if self.channel_id is None:
            await ctx.send("El canal de destino no está configurado. Usa el comando `setupVPS` para configurarlo.")
            return
        info = await self.request_info(ctx)  # Solicitar información al usuario
        if info:
            await self.send_vps_template(ctx, info)  # Enviar la plantilla con la información proporcionada

    async def send_vps_template(self, ctx, info):
        """Envía la plantilla con la información proporcionada al canal designado."""
        if self.channel_id is None:
            await ctx.send("El canal de destino no está configurado. Usa el comando `setupVPS` para configurarlo.")
            return
        # Crear la plantilla utilizando la información proporcionada por el usuario
        template = f"""
# INFORMATION NECESSARY FOR HOSTING IN MY VPS
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
        # Verificar si el canal de destino existe
        if canal_destino:
            # Enviar la plantilla al canal de destino
            await canal_destino.send(template)
        else:
            await ctx.send("No se encontró el canal de destino.")

# Función para configurar el cog dentro del bot
async def setup(bot):
    await bot.add_cog(VPS(bot))