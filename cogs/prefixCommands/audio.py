import gtts
import asyncio
import discord
from discord.ext import commands


class Reproducer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="audio", aliases=["a"] )
    async def audio(self, ctx, *, texto):
        canal_de_voz = ctx.author.voice.channel

        if not canal_de_voz:
            await ctx.send("You must be in a voice channel to use this command.")
            return

        canal_de_voz_client = await canal_de_voz.connect()
        canal_de_voz_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=self.texto_a_audio(texto)))

        while canal_de_voz_client.is_playing():
            await asyncio.sleep(10)

        await canal_de_voz_client.disconnect()

    def texto_a_audio(self, texto):  

        tts = gtts.gTTS(texto, lang='es')
        tts.save('tts_audio.mp3')

        return 'tts_audio.mp3'

async def setup(bot):
    await bot.add_cog(Reproducer(bot)) 
