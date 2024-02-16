import discord
from discord.ext import commands
import wolframalpha
import os
from dotenv import load_dotenv  # Importa load_dotenv

# Carga las variables de entorno
load_dotenv()
wolframapi = os.getenv('MOMO_WOLFRAM_API')

class Wolfram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Usa la variable de entorno para la clave de API de Wolfram Alpha
        self.wolfram_client = wolframalpha.Client(wolframapi)

    @commands.command(name='wolfram', aliases=["w"])
    async def wolfram(self, ctx, *, query: str): 
        try:
            res = self.wolfram_client.query(query)
            answer = next(res.results).text
            
            # Crea un embed con la respuesta
            embed = discord.Embed(title="Wolfram Alpha Resultado", color=0xFFD1DC)
            embed.add_field(name="<:momomoon:1206265862684672101> Question", value=query, inline=False)
            embed.add_field(name="<:momostar:1206265916472692839> Awnswer", value=answer, inline=False)
            
            # Añade el ícono de Wolfram Alpha al embed
            embed.set_thumbnail(url="https://www.wolframalpha.com/_next/static/images/share_3G6HuGr6.png")

            # Envía el embed en el canal
            await ctx.send(embed=embed)

        except StopIteration:
            embed = discord.Embed(title="Wolfram Alpha Resultado", description="Lo siento, no tengo una respuesta para eso.", color=0xFDB9C8)
            embed.set_thumbnail(url="https://www.wolframalpha.com/_next/static/images/share_3G6HuGr6.png")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"Ocurrió un error: {str(e)}", color=0xff0000)
            embed.set_thumbnail(url="https://www.wolframalpha.com/_next/static/images/share_3G6HuGr6.png")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Wolfram(bot))