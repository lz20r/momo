import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
  
class Series(commands.Cog, name="Series de Anime"):
    def __init__(self, bot): 
        self.bot = bot

    @commands.command(name="seasons", aliases=["ss", "seasons_anime", "seasons_anime_es"])
    async def seasons(self, ctx):
        url = "https://www.livechart.me/spring-2024/tv" 
        
        try:
            response = requests.get(url) 
            soup = BeautifulSoup(response.text, "html.parser")
            
            nuevas_temporadas = []
            
            for anime in soup.find_all("div", class_="anime-card"):
                title = anime.find("a", class_="title").text
                nuevas_temporadas.append(title)
            
            if nuevas_temporadas:
                await ctx.send("Nuevas temporadas de anime:")
                await ctx.send("\n".join(nuevas_temporadas))
            else:
                await ctx.send("No se encontraron nuevas temporadas de anime.")
        
        except Exception as e:
            await ctx.send(f"Ocurrió un error al consultar nuevas temporadas de anime: {e}")

# Agregar el Cog al bot
async def setup(bot):
    await bot.add_cog(Series(bot))
 