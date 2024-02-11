import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import random
import io

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_process = {}

    # Función para generar un captcha aleatorio como imagen
    def generate_captcha_image(self):
        # Crear una imagen en blanco
        image = Image.new('RGB', (200, 50), color = (255, 255, 255))
        font = ImageFont.truetype("arial.ttf", 30)
        draw = ImageDraw.Draw(image)

        # Generar el texto del captcha
        captcha_text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))

        # Dibujar el texto en la imagen
        draw.text((10, 10), captcha_text, fill=(0,0,0), font=font)

        # Guardar la imagen en un buffer de bytes
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        return captcha_text, img_byte_array

    @commands.command(name="verify", aliases=["varify"])
    async def setVerify(self, ctx):
        # Verificar que el usuario no esté ya en proceso de verificación
        if ctx.author.id in self.verification_process:
            await ctx.send("Ya estás en proceso de verificación.")
            return

        # Generar el captcha y almacenar el usuario y su captcha en el diccionario
        captcha_text, captcha_image = self.generate_captcha_image()
        self.verification_process[ctx.author.id] = captcha_text

        # Enviar la imagen del captcha al usuario
        await ctx.send(f"{ctx.author.mention}, ingresa el siguiente captcha para verificar:")
        await ctx.send(file=discord.File(captcha_image, "captcha.png"))

    @commands.Cog.listener()
    async def on_message(self, message):
        # Verificar si el mensaje es del usuario en proceso de verificación
        if message.author.id in self.verification_process:
            # Verificar si el mensaje es el captcha correcto
            if message.content == self.verification_process[message.author.id]:
                # Remover al usuario del proceso de verificación
                del self.verification_process[message.author.id]
                
                # Eliminar el rol anterior del usuario
                for role in message.author.roles:
                    if role.name != "@everyone":
                        await message.author.remove_roles(role)
                
                # Asignar un rol verificado al usuario (reemplaza 'role_id' con el ID del rol)
                role = message.guild.get_role(role_id)
                await message.author.add_roles(role)
                
                await message.channel.send(f"{message.author.mention} ha sido verificado correctamente.")
            else:
                await message.channel.send("Captcha incorrecto. Inténtalo de nuevo.")

async def setup(bot):
    await bot.add_cog(Verification(bot))