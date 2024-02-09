import discord
from discord.ext import commands
import json
import os

class setWelcm(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = "Momo Data"  
        os.makedirs(self.data_folder, exist_ok=True)  
        self.json_file_path = os.path.join(self.data_folder, 'WelcomeEmbedCreated.json')
        self.color_pastel = 0xFFC0CB

        try:
            with open(self.json_file_path, 'r') as f: 
                self.welcome_embeds = json.load(f)
        except FileNotFoundError:
            self.welcome_embeds = {}
             
    @commands.command(name="setwlcm", aliases=["sw", "set_wl", "set_wlc", "set_welcome", "set_wlcm"])
    async def set_welcome_embed(self, ctx):
        """Personaliza tu propio mensaje de bienvenida en forma de embed."""
        await ctx.send("Por favor, sigue las instrucciones a continuación para personalizar tu mensaje de bienvenida en forma de embed.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("Por favor, introduce el título de tu mensaje de bienvenida:")
        title_msg = await self.bot.wait_for("message", check=check, timeout=60)

        await ctx.send("Por favor, introduce la descripción de tu mensaje de bienvenida:")
        description_msg = await self.bot.wait_for("message", check=check, timeout=60)

        embed = discord.Embed(
            title=title_msg.content,
            description=description_msg.content
        )

        await ctx.send("¿Deseas agregar un campo al mensaje de bienvenida? (Sí/No)")
        add_field_msg = await self.bot.wait_for("message", check=check, timeout=60)

        while add_field_msg.content.lower() == "sí":
            await ctx.send("Por favor, introduce el nombre del campo:")
            field_name_msg = await self.bot.wait_for("message", check=check, timeout=60)

            await ctx.send("Por favor, introduce el valor del campo:")
            field_value_msg = await self.bot.wait_for("message", check=check, timeout=60)

            embed.add_field(
                name=field_name_msg.content,
                value=field_value_msg.content,
                inline=False
            )

            await ctx.send("¿Deseas agregar otro campo? (Sí/No)")
            add_field_msg = await self.bot.wait_for("message", check=check, timeout=60)

        self.welcome_embeds[str(ctx.guild.id)] = embed.to_dict()
        self.save_welcome_embeds_to_json()
        await ctx.send("Mensaje de bienvenida personalizado guardado correctamente.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if str(guild.id) in self.welcome_embeds:
            embed_data = self.welcome_embeds[str(guild.id)]
            embed = discord.Embed.from_dict(embed_data)
            await member.send(embed=embed)

    def save_welcome_embeds_to_json(self):
        with open(self.json_file_path, 'w') as f:
            json.dump(self.welcome_embeds, f, indent=4)
async def setup(bot):
    await bot.add_cog(setWelcm(bot))
