import discord
from discord.ext import commands
import json
import os

class SelfPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = "Momo Data"
        os.makedirs(self.data_folder, exist_ok=True)
        self.file_path = os.path.join(self.data_folder, "MomoSelfPrefix.json")  # Ruta al archivo JSON
        self.prefixes = {}

    async def read_json(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        else:
            return {}

    async def write_json(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        self.prefixes = await self.read_json()

    @commands.command(name="selfprefix", aliases=["sfp"])
    async def selfprefix(self, ctx, *, new_prefix):
        """Establece un nuevo prefijo personalizado."""
        self.prefixes[str(ctx.guild.id)] = new_prefix  # Almacenar el nuevo prefijo en el diccionario
        await self.write_json(self.prefixes)
        await ctx.send(f"El prefijo ha sido actualizado a: {new_prefix}")

    async def get_prefix(self, bot, message):
        guild_id = str(message.guild.id)
        return self.prefixes.get(guild_id, "!")  # Prefijo predeterminado si no se encuentra uno personalizado

bot = commands.Bot(command_prefix=commands.AutoShardedBot.get_prefix)  # Usamos una función para obtener el prefijo

async def setup(bot):
    await bot.add_cog(SelfPrefix(bot)) 
