import discord
from discord.ext import commands

# Creamos una clase para nuestro cog
class VPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None  # Inicializamos el ID del canal como None

    @commands.command(name="setup_vpsChannel", aliases=["vCh"])
    @commands.has_permissions(administrator=True)
    async def setup_vps(self, ctx, channel: discord.TextChannel):
        """Configura el canal donde se enviarán las plantillas rellenadas."""
        self.channel_id = channel.id
        await ctx.send(f"Canal configurado correctamente como {channel.mention} para enviar las plantillas rellenadas.")

    @commands.command(name="vpsTemplate", aliases=["vpsT"])
    @commands.has_permissions(administrator=True)
    async def vpsTemplate(self, ctx, mail=None, username=None, first_name=None, last_name=None, password=None, server_name=None, cpu=None, ram=None, disk=None, egg=None): 
        if self.channel_id is None:
            await ctx.send("El canal de destino no está configurado. Usa el comando `setup_vps` para configurarlo.")
            return 
        # Verificamos si se proporcionaron todos los datos requeridos
        if any(arg is None for arg in [mail, username, first_name, last_name, password, server_name, cpu, ram, disk, egg]):
            await ctx.send("Debes proporcionar todos los datos requeridos.")
            return

        # Obtenemos la mención y el ID del usuario
        user_mention = ctx.author.mention
        user_id = ctx.author.id

        # Creamos la plantilla con los datos proporcionados por el usuario
        template = f"""
        # INFORMATION NECESSARY FOR HOSTING IN MY VPS
        **{user_mention} -- {user_id}**
        **{user_mention} Credentials:**
         - Mail: {mail}
         - Username: {username}
         - First Name: {first_name}
         - Last Name: {last_name}
         - Password: {password}
        ————-————-————-————-————
        - **Core Details**   
            - Server Name: {server_name}
        - **Allocation Management** 
         - CPU: {cpu}
         - RAM: {ram}
         - Disk: {disk}
        - **Node**
            - Egg (Lenguaje que usa tu bot): {egg}
        """

        # Obtener el canal de destino
        canal_destino = ctx.guild.get_channel(self.channel_id)

        # Verificar si el canal de destino existe
        if canal_destino:
            # Enviar la plantilla rellenada al canal de destino
            await canal_destino.send(template)
        else:
            await ctx.send("No se encontró el canal de destino.")

# Función para configurar el cog dentro del bot
async def setup(bot):
    await bot.add_cog(VPS(bot)) 