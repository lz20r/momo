import discord
import os
import json
from discord import Embed
from discord.ext import commands
from discord.ui import View, Button

class prefix_manual(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.data_folder = "Momo Data"
        os.makedirs(self.data_folder, exist_ok=True)
        self.prefix_file_path = os.path.join(self.data_folder, 'Momoprefix.json')

    async def save_prefixes(self, server_prefixes):
        with open(self.prefix_file_path, "w") as file: 
            json.dump(server_prefixes, file, indent=4)
            
    async def load_prefixes(self):
        try:
            with open(self.prefix_file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @commands.command(name='setPrefix', aliases=['sp', 'serverprefix'])
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, new_prefix=None):
        server_id = str(ctx.guild.id)
        server_name = ctx.guild.name
        user_name = ctx.author.name
        
        if new_prefix is None:
            embed = discord.Embed(description="Provide the prefix to set")
            return await ctx.send(embed=embed)

        # Cargar los prefijos personalizados actuales
        server_prefixes = await self.load_prefixes()

        # Establecer el nuevo prefijo y guardar los cambios
        server_prefixes[server_id] = {
            "server_name": server_name,
            "user_name": user_name,
            "prefix": new_prefix
        }

        await self.save_prefixes(server_prefixes)

        embed = discord.Embed(description=f"Server prefix set to `{new_prefix}`")
        await ctx.send(embed=embed)

async def setup(bot): 
    await bot.add_cog(prefix_manual(bot))   