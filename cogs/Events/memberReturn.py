'''
import random
import discord
from discord.ext import commands

class Rejoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.welcome_channels = {}  
        self.return_messages = [  
            "Welcome back {mention} to {server}!",
            "{server} was waiting for you. Welcome back {mention}!",
            "{mention}, welcome back to {server}!",
            "Thank you so much for trusting us. Welcome back {mention}!",
            "We will try to give you a better service. Welcome back {mention}!",
            "Welcome back to {server}, {mention}!",
        ]
        
    def generate_pastel_color(self):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        return (r << 16) + (g << 8) + b
     
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = self.welcome_channels.get(member.guild.id)
        if channel_id:
            channel = self.bot.get_channel(channel_id)
        else:
            channel = next((ch for ch in member.guild.text_channels if ch.permissions_for(member.guild.me).send_messages), None)
                
        if channel:  # Verificar si se encontró un canal
            return_text = random.choice(self.return_messages).format(mention=member.mention)
            return_count = f"Total Cinammon Members: {member.guild.member_count}"
            embed_color = self.generate_pastel_color()  # Generar un color pastel aleatorio
            
            embed = discord.Embed(description=return_text, color=embed_color)
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            embed.set_footer(text=f"Cinammon | Your Trusted Host! | {return_count}")
            
            try:
                await channel.send(embed=embed)
            except Exception as e:
                print(f"Error al enviar mensaje de bienvenida: {e}")
        else:
            print("No se encontró un canal adecuado para enviar el mensaje de bienvenida.")
    
    @commands.command(name='setrejoin', aliases=['srejoin'], help='Establece el canal de bienvenida para miembros que regresan.')
    @commands.has_permissions(administrator=True)
    async def set_return_channel(self, ctx, channel: discord.TextChannel):
        self.welcome_channels[ctx.guild.id] = channel.id
        await ctx.send(f'El canal de bienvenida se ha establecido en: {channel.mention}')
        
    @commands.command(name='delrejoin', aliases=['drejoin'], help='Elimina el canal de bienvenida para miembros que regresan.')
    @commands.has_permissions(administrator=True)
    async def del_return_channel(self, ctx):
        if ctx.guild.id in self.welcome_channels:
            self.welcome_channels.pop(ctx.guild.id)
            await ctx.send('El canal de bienvenida ha sido eliminado.')
        else:
            await ctx.send('No se ha configurado un canal de bienvenida.')
        
async def setup(bot):
    await bot.add_cog(Rejoin(bot))

'''

