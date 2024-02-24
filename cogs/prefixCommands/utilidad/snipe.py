from math import e
import random
from re import T
from sys import prefix
import discord
from discord.ext import commands
from httpx import get

from cogs.prefixCommands.setup.setPrefix import Prefix

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_messages = [] 
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.content:
            return

        self.deleted_messages.insert(0, (message.content, message.author, message.channel, message.created_at))
        if len(self.deleted_messages) > 100:
            self.deleted_messages.pop(-1)

    @commands.command(name="history", aliases=["sh"])
    async def history(self, ctx):
        if not self.deleted_messages:
            embed = discord.Embed(title="Historial de Mensajes Borrados", description="No hay mensajes borrados recientemente.", color=random_pastel_color())
            ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Historial de Mensajes Borrados", description="Aquí están los últimos mensajes borrados:", color=random_pastel_color())
        embed.set_author(name="Snipe", icon_url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Comando usado por {ctx.author}")
        for i, (content, author, channel, time) in enumerate(self.deleted_messages[:100], start=1):
            embed.add_field(name=f"Mensaje {i}", value=f"**Autor:** {author.display_name}\n**Canal:** {channel.mention}\n\n**Contenido:** {content[:100]}{'...' if len(content) > 100 else ''}", inline=True) 
        await ctx.send(embed=embed)
        

    @commands.command(name="snipeEmbed", aliases=["sE"])
    async def snipeEmbed(self, ctx, index: int = 1):
        index -= 1
        if 0 <= index < len(self.deleted_messages):
            content, author, channel, time = self.deleted_messages[index]
            if channel == ctx.channel:
                embed = discord.Embed(description=content, timestamp=time, color=random_pastel_color())
                embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)
                embed.set_footer(text=f"Borrado en {channel} | Mensaje {index + 1} de {len(self.deleted_messages)}")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description="Este mensaje fue borrado en otro canal.", color=random_pastel_color())
                embed.set_footer(text=f"Borrado en {channel} | Mensaje {index + 1} de {len(self.deleted_messages)}")
                await channel.send(embed=embed)  
        else:
            embed = discord.Embed(description="Número de mensaje inválido. Usa un número entre 1 y 10.", color=random_pastel_color())
            embed.set_footer(text=f"Borrado en {channel} | Mensaje {index + 1} de {len(self.deleted_messages)}")
            await ctx.send(embed=embed)
    
    @commands.command(name="snipeNormal", aliases=["sN"])
    async def snipeNormal(self, ctx, index: int = 1):
        index -= 1
        if 0 <= index < len(self.deleted_messages):
            content, author, channel, time = self.deleted_messages[index]
            if channel == ctx.channel:
                await ctx.send(f" **Autor:** {author.display_name} \n" + "**Canal:** " + channel.mention + "\n\n" + "**Contenido:** \n" + content)  
            else: 
                embed = discord.Embed(description="Este mensaje fue borrado en otro canal.", color=random_pastel_color())
                embed.set_footer(text=f"Borrado en {channel} | Mensaje {index + 1} de {len(self.deleted_messages)}")
                await channel.send(embed=embed) 
        else: 
            ctx.send("Número de mensaje inválido. Usa un número entre 1 y 10.")
            
    @commands.command(name="clearsnipe", aliases=["cs"])
    async def clear_snipe(self, ctx):
        self.deleted_messages = []
        await ctx.send("Historial de mensajes borrados limpiado.")
        
    @commands.command(name="snipe", aliases=["shelp"])
     
    async def snipe_help(self, ctx):   
        embed = discord.Embed(title="Comandos Snipe", color=random_pastel_color())
        embed.add_field(name=f"snipeNormal", value="Muestra el contenido de un mensaje borrado.", inline=False)
        embed.add_field(name=f"snipeEmbed", value="Muestra un embed de un mensaje borrado.", inline=False)
        embed.add_field(name=f"clearsnipe", value="Limpia el historial de mensajes borrados.", inline=False)
        embed.add_field(name=f"history", value="Muestra el historial de mensajes borrados.", inline=False)
        embed.set_footer(text="Comandos Snipe")
        embed.set_author(name="Snipe", icon_url=self.bot.user.avatar.url) 
        await ctx.send(embed=embed)
         
def random_pastel_color():
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    return discord.Colour.from_rgb(r, g, b)

async def setup(bot):
    await bot.add_cog(Snipe(bot)) 
