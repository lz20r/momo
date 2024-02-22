import discord
from discord.ext import commands
import lavalink 

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando play dentro del Cog
    @commands.command( name='play', aliases=['p'] )
    async def play(self, ctx, *, query: str):
        # Busca la pista en YouTube
        tracks = await wavelink.YouTubeTrack.search(query)

        if not tracks:
            return await ctx.send('No se encontraron canciones con ese nombre.')

        track = tracks[0]  # Obtiene el primer resultado

        # Conecta al bot al canal de voz si no está conectado
        if not ctx.voice_client:
            vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc = ctx.voice_client

        # Reproduce la pista
        await vc.play(track)
        await ctx.send(f'Reproduciendo: {track.title}')

# Función para cargar el Cog
async def setup(bot):
    await bot.add_cog(Music(bot))
 