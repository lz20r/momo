import discord
from discord.ext import commands
import os
import json

class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.data_folder = "Momo Data"
        os.makedirs(self.data_folder, exist_ok=True)
        self.prefix_file_path = os.path.join(self.data_folder, 'Momoprefix.json')
        self.server_prefixes = self.load_prefixes()

        bot.command_prefix = self.get_dynamic_prefix

    async def get_dynamic_prefix(self, bot, message):
        server_id = str(message.guild.id)
        if server_id in self.server_prefixes:
            return self.server_prefixes[server_id]["prefix"]
        return "m."  # Prefijo por defecto

    async def save_prefixes(self):
        with open(self.prefix_file_path, "w") as file:
            json.dump(self.server_prefixes, file, indent=4)

    def load_prefixes(self):
        try:
            with open(self.prefix_file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @commands.command(name='setPrefix', aliases=['sp', 'serverprefix'])
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, new_prefix=None):
        if new_prefix is None:
            embed = discord.Embed(description="Please provide a prefix to set.")
            return await ctx.send(embed=embed)

        server_id = str(ctx.guild.id)
        server_name = ctx.guild.name
        user_name = ctx.author.name

        self.server_prefixes[server_id] = {
            "server_name": server_name,
            "user_name": user_name,
            "prefix": new_prefix
        }

        await self.save_prefixes()

        embed = discord.Embed(description=f"Prefix for **{server_name}** set to `{new_prefix}` by **{user_name}**.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Prefix(bot)) 