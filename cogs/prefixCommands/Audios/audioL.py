import gtts
import asyncio
import discord
from discord.ext import commands
import os
import json
from langdetect import detect
import time

class Reproducer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_logs_path = "Momo Data/MomoAudioLogsLanguages"
        if not os.path.exists(self.audio_logs_path):
            os.makedirs(self.audio_logs_path)
        self.usage_log_file = os.path.join(self.audio_logs_path, "MomoUsageLogsLanguages.json")

    @commands.command(name="audioL", aliases=["aL", "aLs"])
    async def audio(self, ctx, *, texto):
        if not ctx.author.voice:
            await ctx.send("You must be in a voice channel to use this command.")
            return

        try:
            canal_de_voz = ctx.author.voice.channel
            canal_de_voz_client = await canal_de_voz.connect()

            # Detectar el idioma del texto
            lang = detect(texto)
            if lang not in gtts.lang.tts_langs():
                lang = 'en'  # Usar inglés como idioma predeterminado si el detectado no es soportado

            # Generar y obtener la ruta del archivo de audio
            audio_file = self.texto_a_audio(texto, ctx.author.name, ctx.guild.name, canal_de_voz.name, lang)

            # Reproducir el audio
            canal_de_voz_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=audio_file))

            while canal_de_voz_client.is_playing():
                await asyncio.sleep(1)

            await canal_de_voz_client.disconnect()

            # Registrar el uso del comando y el archivo de audio
            self.registrar_uso(ctx.author.name, ctx.guild.name, canal_de_voz.name, texto, lang)
            self.actualizar_indice_audio(audio_file)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            if canal_de_voz_client and canal_de_voz_client.is_connected():
                await canal_de_voz_client.disconnect()

    def texto_a_audio(self, texto, user_name, server_name, channel_name, lang):
        tts = gtts.gTTS(texto, lang=lang)
        audio_file_name = f"tts_{user_name}_{server_name}_{channel_name}_{lang}_{int(time.time())}.mp3"
        audio_file_path = os.path.join(self.audio_logs_path, audio_file_name)
        tts.save(audio_file_path)
        return audio_file_path

    def registrar_uso(self, user_name, server_name, channel_name, texto, lang):
        data = {
            "user_name": user_name,
            "server_name": server_name,
            "channel_name": channel_name,
            "texto": texto,
            "idioma": lang,
            "timestamp": int(time.time())
        }

        if os.path.exists(self.usage_log_file):
            with open(self.usage_log_file, "r") as file:
                log_data = json.load(file)
        else:
            log_data = []

        log_data.append(data)

        with open(self.usage_log_file, "w") as file:
            json.dump(log_data, file, indent=4)

    def actualizar_indice_audio(self, audio_file_path):
        audio_index_file = os.path.join(self.audio_logs_path, "audio_index.json")
        if os.path.exists(audio_index_file):
            with open(audio_index_file, "r") as file:
                audio_index = json.load(file)
        else:
            audio_index = []

        audio_index.append(audio_file_path)

        with open(audio_index_file, "w") as file:
            json.dump(audio_index, file, indent=4)

async def setup(bot):
    await bot.add_cog(Reproducer(bot)) 