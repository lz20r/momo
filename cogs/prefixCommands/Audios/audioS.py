import gtts
import asyncio
import discord
from discord.ext import commands


class Reproductor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(name="audio", aliases=["a", "as", "ads"] )
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
        supported_langs = ['af', 'sq', 'ar', 'hy', 'bn', 'ca', 'zh', 'zh-cn', 'zh-tw', 'zh-yue', 'hr', 'cs', 'da', 'nl', 'en', 'en-au', 'en-uk', 'en-us', 'eo', 'fi', 'fr', 'de', 'el', 'hi', 'hu', 'is', 'id', 'it', 'ja', 'km', 'ko', 'la', 'lv', 'mk', 'no', 'pl', 'pt', 'ro', 'ru', 'sr', 'si', 'sk', 'es', 'es-es', 'es-us', 'sw', 'sv', 'ta', 'th', 'tr', 'uk', 'vi', 'cy']
    
    # Verificar si el idioma detectado es compatible, de lo contrario, usar inglés como predeterminado
    if lang not in supported_langs:
        lang = 'en'  # Idioma predeterminado        

        tts = gtts.gTTS(texto, lang='es')
        tts.save('tts_audio.mp3')

        return 'tts_audio.mp3'

async def setup(bot):
    await bot.add_cog(Reproductor(bot)) 