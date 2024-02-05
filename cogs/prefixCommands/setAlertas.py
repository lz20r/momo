import discord
from discord.ext import commands
import json

# Diccionario para almacenar las preferencias de alerta de los usuarios
user_alerts = {}

# Definir una clase para el menú de configuración
class Alertas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="setAlets", aliases=["setupAlets", "sA"]) 
    async def configure_alerts(self, ctx):
        user_id = ctx.author.id
        if user_id not in user_alerts:
            user_alerts[user_id] = {"instagram": False, "youtube": False, "whatsapp": False}

        embed = discord.Embed(title="Configuración de Alertas", color=0x42f56c)
        embed.add_field(name="1️⃣ Instagram", value="Activa o desactiva alertas de Instagram", inline=False)
        embed.add_field(name="2️⃣ YouTube", value="Activa o desactiva alertas de YouTube", inline=False)
        embed.add_field(name="3️⃣ WhatsApp", value="Activa o desactiva alertas de WhatsApp", inline=False)
        embed.set_footer(text="Responde con el número correspondiente para configurar")

        await ctx.send(embed=embed)

        def check(msg):
            return msg.author == ctx.author and msg.content.isdigit() and 1 <= int(msg.content) <= 3

        try:
            response = await self.bot.wait_for("message", check=check, timeout=30)
            option = int(response.content)
            if option == 1:
                user_alerts[user_id]["instagram"] = not user_alerts[user_id]["instagram"]
                await ctx.send(f"Alertas de Instagram {'activadas' if user_alerts[user_id]['instagram'] else 'desactivadas'}.")
            elif option == 2:
                user_alerts[user_id]["youtube"] = not user_alerts[user_id]["youtube"]
                await ctx.send(f"Alertas de YouTube {'activadas' if user_alerts[user_id]['youtube'] else 'desactivadas'}.")
            elif option == 3:
                user_alerts[user_id]["whatsapp"] = not user_alerts[user_id]["whatsapp"]
                await ctx.send(f"Alertas de WhatsApp {'activadas' if user_alerts[user_id]['whatsapp'] else 'desactivadas'}.")
            
            # Almacena los datos en un archivo JSON
            with open("Momo Data/alerts.json", "a") as json_file:
                json.dump(user_alerts, json_file)
                json_file.write("\n")  # Agrega un salto de línea para el siguiente dato
                
        except asyncio.TimeoutError:
            await ctx.send("La configuración ha expirado. Vuelve a intentarlo más tarde.")

# Comando para obtener información de alertas
@commands.command(name="getalertsinfo", aliases=["gai"])
async def get_alerts(ctx):
    user_id = ctx.author.id
    if user_id in user_alerts:
        alerts_info = user_alerts[user_id]
        await ctx.send(f"Tus alertas:\n"
                       f"Instagram: {'Activadas' if alerts_info['instagram'] else 'Desactivadas'}\n"
                       f"YouTube: {'Activadas' if alerts_info['youtube'] else 'Desactivadas'}\n"
                       f"WhatsApp: {'Activadas' if alerts_info['whatsapp'] else 'Desactivadas'}")
    else:
        await ctx.send("No has configurado tus alertas. Usa el comando `config` para configurarlas.")

# Función para agregar la cog Menu al bot (añadida)
async def setup(bot):
    await bot.add_cog(Alertas(bot))