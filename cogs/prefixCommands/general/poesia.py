import discord
from discord.ext import commands
import random

def pastel_color():
    r = random.randint(180, 255)
    g = random.randint(180, 255)
    b = random.randint(180, 255)
    return discord.Color.from_rgb(r, g, b)

class Poesia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poesia")
    async def send_poesia(self, ctx, *, args):
        color = pastel_color()
        try:
            parts = args.split(maxsplit=1)
            user_id = int(parts[0])  # Intenta convertir la primera parte en un entero
            poesia = parts[1]  # El resto de los argumentos se considera la poesía
        except ValueError:
            # Si la conversión falla o no hay suficientes partes, envía un mensaje de error
            await ctx.send("Uso incorrecto del comando. Formato: `m.poesia <user_id> <poesia>`")
            return

        # Procede como antes con el user_id y poesia
        try:
            user = await self.bot.fetch_user(user_id)
        except discord.NotFound:
            await ctx.send(f"No se pudo encontrar un usuario con el ID {user_id}.")
            return
        except discord.HTTPException as e:
            await ctx.send(f"Ocurrió un error al intentar obtener el usuario: {e}")
            return

        embed = discord.Embed(title="Una Poesía para Ti", description=poesia, color=color)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text="Poesía enviada desde el bot")

        try:
            await user.send(embed=embed)
            await ctx.send(f"Poesía enviada correctamente a {user.name}.")
        except discord.Forbidden:
            await ctx.send(f"No se pudo enviar un DM a {user.name}.")
        except discord.HTTPException as e:
            await ctx.send(f"Ocurrió un error al intentar enviar el DM: {e}")

async def setup(bot):
    await bot.add_cog(Poesia(bot))