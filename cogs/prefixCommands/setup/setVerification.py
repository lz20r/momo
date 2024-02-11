import io
import os
import random
import discord
from discord.ext import commands
from discord.ui import View, Button
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_process = {}
        self.gif_dir = "./animes.txt"
        self.role_id = 1202058820361125888
        self.new_role_id = 1202241653247836180

    def get_random_anime_gif(self):
        gifs = os.listdir(self.gif_dir)
        gif_name = random.choice(gifs)
        return os.path.join(self.gif_dir, gif_name)

    def generate_captcha_gif(self):
        anime_gif_path = self.get_random_anime_gif()
        anime_clip = VideoFileClip(anime_gif_path)
        captcha_text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890*+-.!"·$%&//()=¿?^¡!;,', k=6))
        fontsize = min(anime_clip.size) // 10
        text_clip = TextClip(captcha_text, fontsize=fontsize, color='white', method='caption', size=anime_clip.size)
        text_clip = text_clip.set_position(('center', 'center')).set_duration(anime_clip.duration)
        composite_clip = CompositeVideoClip([anime_clip, text_clip])
        gif_byte_array = io.BytesIO()
        composite_clip.write_gif(gif_byte_array, fps=anime_clip.fps)
        gif_byte_array.seek(0)
        return captcha_text, gif_byte_array

    @commands.command()
    async def setVerify(self, ctx):
        if ctx.author.id in self.verification_process:
            await ctx.send("You already have a verification process in progress.", ephemeral=True)
            return
        captcha_text, captcha_gif = self.generate_captcha_gif()
        self.verification_process[ctx.author.id] = captcha_text, captcha_gif

        # Crear el mensaje embed
        embed = discord.Embed(title="<:momostarw:1206266007090364486> Momo Verify Sytem", description=f"{ctx.author.mention}, fill the captcha below to verify your account.")
        embed.set_image(url="attachment://captcha.gif")  # Adjuntar el gif al mensaje embed

        # Enviar el mensaje embed con el gif y el botón de Momo Verify Sytem
        await ctx.send(embed=embed, file=discord.File("captcha.gif", "captcha.gif"), view=VerificationView())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.verification_process:
            if message.content == self.verification_process[message.author.id]:
                del self.verification_process[message.author.id]
                for role in message.author.roles:
                    if role.name != "members":
                        await message.author.remove_roles(role)
                role_id = self.new_role_id
                role = message.guild.get_role(role_id)
                await message.author.add_roles(role)
                embed = discord.Embed(title="Momo Verify Sytem", description=f"<:cinnaexcited:1205894714679885895> {message.author.mention}: your account has been verified successfully, by {self.bot.user.mention}")
                embed.set_footer(text="<:momostarw:1206266007090364486> Momo Verify Sytem")
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Momo Verify Sytem", description=f"\<:cinnacry:1205894709944254514> you made an incorrect captcha, try again.  {self.bot.user.mention} will tell to the owner.")
                embed.set_footer(text="<:momostarw:1206266007090364486> Momo Verify Sytem")
                await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Verification(bot))

class VerificationView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(style=ButtonStyle.blue, label="Verify"))

    @discord.ui.button(label="Verify", style=ButtonStyle.blue)
    async def verify_button(self, button: discord.ui.Button, interaction: discord.Interaction): 
        button.emoji = "<:cinnaexcited:1205894714679885895>"
        await interaction.response.edit_message("Verified!", ephemeral=True)
        



'''
    import io
    import random
    import discord
    from discord.ext import commands
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
    import os

    class Verification(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            self.verification_process = {}
            self.gif_dir = "./animes.txt"

        # Función para seleccionar aleatoriamente un gif de anime
        def get_random_anime_gif(self):
            gifs = os.listdir(self.gif_dir)
            gif_name = random.choice(gifs)
            return os.path.join(self.gif_dir, gif_name)

        # Función para generar un captcha aleatorio como gif
        def generate_captcha_gif(self):
            # Seleccionar un gif de anime aleatorio
            anime_gif_path = self.get_random_anime_gif()

            # Cargar el gif y agregar el texto del captcha
            anime_clip = VideoFileClip(anime_gif_path)
            captcha_text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))
            text_clip = TextClip(captcha_text, fontsize=30, color='white').set_position(('center', 'bottom')).set_duration(anime_clip.duration)
            composite_clip = CompositeVideoClip([anime_clip, text_clip])

            # Guardar el gif en un buffer de bytes
            gif_byte_array = io.BytesIO()
            composite_clip.write_gif(gif_byte_array, fps=anime_clip.fps)
            gif_byte_array.seek(0)

            return captcha_text, gif_byte_array

        @commands.command()
        async def setVerify(self, ctx):
            # Verificar que el usuario no esté ya en proceso de Momo Verify Sytem
            if ctx.author.id in self.verification_process:
                await ctx.send("Ya estás en proceso de Momo Verify Sytem.")
                return

            # Generar el captcha y almacenar el usuario y su captcha en el diccionario
            captcha_text, captcha_gif = self.generate_captcha_gif()
            self.verification_process[ctx.author.id] = captcha_text

            # Enviar el gif del captcha al usuario
            await ctx.send(f"{ctx.author.mention}, ingresa el siguiente captcha para verificar:")
            await ctx.send(file=discord.File(captcha_gif, "captcha.gif"))

        @commands.Cog.listener()
        async def on_message(self, message):
            # Verificar si el mensaje es del usuario en proceso de Momo Verify Sytem
            if message.author.id in self.verification_process:
                # Verificar si el mensaje es el captcha correcto
                if message.content == self.verification_process[message.author.id]:
                    # Remover al usuario del proceso de Momo Verify Sytem
                    del self.verification_process[message.author.id]
                    
                    # Eliminar el rol anterior del usuario
                    for role in message.author.roles:
                        if role.name != "@everyone":
                            await message.author.remove_roles(role)
                    
                    # Asignar un rol verificado al usuario (reemplaza 'role_id' con el ID del rol)
                    role_id = 1234567890  # Reemplaza con el ID del rol
                    role = message.guild.get_role(role_id)
                    await message.author.add_roles(role)
                    
                    await message.channel.send(f"{message.author.mention} ha sido verificado correctamente.")
                else:
                    await message.channel.send("Captcha incorrecto. Inténtalo de nuevo.")

    async def setup(bot):
        await bot.add_cog(Verification(bot)) 

'''
