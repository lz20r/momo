import discord
from discord.ext import commands, tasks
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio

class Files(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._start_file_watcher()

    def _start_file_watcher(self):
        path_to_watch = '/home/container/momo.py'  # Actualiza esto a la ruta de tu archivo
        self.event_handler = FileChangeHandler(self.bot, self._on_file_modified)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=path_to_watch, recursive=False)
        self.observer.start()

    async def _on_file_modified(self):
        channel_id = tu_id_de_canal  # Reemplaza esto con el ID del canal donde quieres enviar las notificaciones
        channel = self.bot.get_channel(1204154596864565259)
        if channel:
            await channel.send("El archivo ha sido modificado.")

    def cog_unload(self):
        self.observer.stop()
        self.observer.join()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, bot, callback):
        self.bot = bot
        self.callback = callback

    def on_modified(self, event):
        asyncio.run_coroutine_threadsafe(self.callback(), self.bot.loop)

async def setup(bot):
    await bot.add_cog(Files(bot))