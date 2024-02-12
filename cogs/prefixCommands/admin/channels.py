import discord
from discord.ext import commands

from main import embed

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel_id = 1204154596864565259  # ID del canal donde quieres enviar los mensajes de éxito
        self.error_channel_id = 1202541792478887936  # ID del canal donde quieres enviar los mensajes de error
        self.pastel_color = 0xadd8e6  # Color pastel predeterminado: azul claro
        self.channel_name = self.target_channel_id

    async def send_embed_message(self, message, channel_id, color=None):
        channel = self.bot.get_channel(channel_id)
        color = color or self.pastel_color  # Si no se proporciona un color, se utiliza el color pastel predeterminado
        embed = discord.Embed(title="Gestión de Canales y Hilos", description=message, color=color)
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        await self.send_embed_message(str(error), self.error_channel_id, color=0xff6666)  # Light red for error

    async def handle_forbidden_error(self):
        error_channel_id = self.error_channel_id
        # Crea un embed para el mensaje de error
        embed = discord.Embed(title="Logs Error", description="No tengo permisos para realizar esta acción.", color=discord.Color.red())

        # Enviar el embed al canal de errores
        error_channel = self.bot.get_channel(error_channel_id)
        await error_channel.send(embed=embed)

    @commands.command(name="CreateChannel", aliases=["CCH", "CrCh", "Cchannel"])
    @commands.has_permissions(administrator=True)    
    async def create_channel(self, ctx, channel_name):
        guild = ctx.guild
        try:
            await guild.create_text_channel(channel_name) 
            embed = discord.Embed(
                title="Canal creado",
                description=f"(El canal {channel_name} ha sido creado.)",
                color=self.color_pastel
            )
            await self.send_embed_message(embed = embed)  # Light green for success
        except discord.Forbidden:
            await self.handle_forbidden_error()
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="DeleteChannel", aliases=["DCH", "DlCh", "Dchannel"])
    @commands.has_permissions(administrator=True)
    async def delete_channel(self, channel: discord.TextChannel):
        try:
            await channel.delete()
            embed = discord.Embed(
                title="Canal eliminado",
                description=f"El canal {channel.name} ha sido eliminado.",
                color=self.color_pastel
            )
            await self.send_embed_message(embed = embed)  # Light green for success
        except discord.Forbidden:
            await self.handle_forbidden_error()
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="UpdateChannel", aliases=["UCH", "UCh", "UChannel"])
    @commands.has_permissions(administrator=True)
    async def update_channel(self, channel: discord.TextChannel, new_name):
        try:
            await channel.edit(name=new_name)
            embed = discord.Embed(
                title="Canal actualizado",
                description=f"El canal {channel.name} con el nuevo nombre {new_name} ha sido actualizado.",
                color=self.color_pastel 
            )
            await self.send_embed_message(embed = embed)  # Light green for success
        except discord.Forbidden:
            await self.handle_forbidden_error()
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="RenameChannel", aliases=["RCH", "RCh", "Rchannel"])
    @commands.has_permissions(administrator=True)
    async def rename_channel(self, channel: discord.TextChannel, new_name):
        try: 
            await channel.edit(name=new_name)
            embed = discord.Embed(
                title="Canal renombrado",
                description=f"El canal {channel.name} con el nuevo nombre {new_name} ha sido renombrado.",
                color=self.color_pastel
            )
            await self.send_embed_message(embed = embed) 
            await self.handle_forbidden_error()
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="CreateThread", aliases=["CrTh"])
    @commands.has_permissions(administrator=True)
    async def create_thread(self, ctx, thread_name):
        try:
            await ctx.channel.create_thread(name=thread_name)
            embed = discord.Embed(
                title="Hilo creado",
                description=f"El hilo {thread_name} ha sido creado.",
                color=self.color_pastel
            )
            await self.send_embed_message(embed = embed) 
        except discord.Forbidden:
            await self.handle_forbidden_error()
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="DeleteThread", aliases=["DlTh"])
    @commands.has_permissions(administrator=True)
    async def delete_thread(self, ctx, thread: discord.Thread):
        try:
            await thread.delete()
            embed = discord.Embed(
                title="Hilo eliminado",
                description=f"El hilo {thread.name} ha sido eliminado.",
                color=self.color_pastel
            )
            await self.send_embed_message(embed = embed)
        except discord.Forbidden:
            await self.handle_forbidden_error()
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="UpdateThread", aliases=["UpTh"])
    @commands.has_permissions(administrator=True)
    async def update_thread(self, thread: discord.Thread, new_name):
        try:
            await thread.edit(name=new_name)
            embed = discord.Embed(
                title="Hilo actualizado",
                description=f"El hilo {thread.name} con el nuevo nombre {new_name} ha sido actualizado.",
                color=self.color_pastel
            )
            await self.send_embed_message(embed = embed)
        except discord.Forbidden:
            await self.handle_forbidden_error()
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="RenameThread", aliases=["RnTh"])
    @commands.has_permissions(administrator=True)
    async def rename_thread(self, ctx, thread: discord.Thread, new_name):
        try:
            await thread.edit(name=new_name)
            embed = discord.Embed(
                title="Hilo renombrado",
                description=f"El hilo {thread.name} con el nuevo nombre {new_name} ha sido renombrado.",
                color=self.color_pastel
            ) 
            await self.send_embed_message(embed = embed)
        except discord.Forbidden:
            await self.handle_forbidden_error()
        except Exception as e:
            await self.send_error_message(e)

async def setup(bot):
    await bot.add_cog(Logs(bot)) 