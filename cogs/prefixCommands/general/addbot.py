import discord
import os
from discord import Embed
from discord.ext import commands
from discord.ui import View, Button

class Addbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addbot(self, ctx, *, link: str):

        if not is_valid_link(link):
            return await ctx.send("Por favor, proporciona un enlace válido.")

        try:
            user = await self.bot.fetch_user(1033160523044376616)
            await user.send(f"¡Aquí tienes un enlace que alguien ha compartido contigo: {link}!")
            await ctx.send("El enlace ha sido enviado exitosamente al usuario 1033160523044376616.")
        except discord.Forbidden:
            await ctx.send("No tengo permiso para enviar mensajes directos a ese usuario.")
        except discord.HTTPException:
            await ctx.send("Ocurrió un error al intentar enviar el enlace.")
            
def is_valid_link(link):
    return True

async def setup(bot): 
    await bot.add_cog(Addbot(bot)) 