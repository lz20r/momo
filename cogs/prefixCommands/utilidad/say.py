import os
import json
import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = "Momo Data" 
        os.makedirs(self.data_folder, exist_ok=True)
        self.file_path = os.path.join(self.data_folder, "MomoSay.json")
        
    async def read_json(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        else:
            return {}

    async def write_json(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    @commands.command(name="say")
    async def say(self, ctx, *, message):
        """Enviar un mensaje a ser mostrado."""
        data = await self.read_json()
        user = str(ctx.author)
        data[user] = message  # Almacenar el mensaje del usuario
        await self.write_json(data)
        await ctx.send(f"{user}: {message}")

    @commands.command()
    async def show(self, ctx):
        """Mostrar los mensajes almacenados."""
        data = await self.read_json()
        if data:
            messages = [f"{user}: {message}" for user, message in data.items()]
            await ctx.send("\n".join(messages))
        else:
            await ctx.send("No hay mensajes almacenados.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Say(bot))