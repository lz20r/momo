import discord
from discord.ext import commands

class PinImageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pinimage', aliases=['ipimg'])
    async def pin_image(self, ctx):
        # Comprobar si el mensaje tiene archivos adjuntos
        if not ctx.message.attachments:
            embed = discord.Embed(description="Por favor, adjunta una imagen al comando.", color=discord.Color.red())
            await ctx.send(embed=embed) 
            return

        # Comprobar permisos del usuario
        if not ctx.message.author.guild_permissions.manage_messages:
            embed = discord.Embed(description="No tienes permisos para fijar mensajes.", color=discord.Color.red())
            await ctx.send(embed=embed) 
            return

        # Comprobar permisos del bot
        if not ctx.guild.me.guild_permissions.manage_messages:
            embed = discord.Embed(description="No tengo permisos para fijar mensajes.", color=discord.Color.red())
            await ctx.send(embed=embed) 
            return

        try:
            # Asumir que el primer archivo adjunto es la imagen
            image = ctx.message.attachments[0]

            # Enviar la imagen
            message = await ctx.send(file=discord.File(fp=await image.to_file()))

            # Fijar (anclar) el mensaje
            await message.pin()

        except discord.HTTPException:
            embed = discord.Embed(description="No pude enviar o fijar la imagen.", color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(bot):
   await bot.add_cog(PinImageCommands(bot))
