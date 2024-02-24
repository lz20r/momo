'''
import random
import discord
from discord.ext import commands

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Asegurarse de que el diccionario para almacenar los canales de despedida esté inicializado
        self.leave_channels = {}
        self.leave_messages = [
            "{server} will be waiting for you for your next visit. Come back soon {mention}!",
            "{mention} has left. {server} will be waiting for you for your next visit."
            "see you {mention} from {server}!",
            "{server} still waiting for you. See you {mention}!",
            "hope you enjoyed your stay. See you {mention}!",
            "maybe next time we can giving you a better service in {server}, tysm for trusting us. See you {mention}!",
            "we hope you could reconsiderate your stay, {server}. see you {mention}!",
        ]
    
    def generate_pastel_color(self):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        return (r << 16) + (g << 8) + b

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel_id = self.leave_channels.get(member.guild.id)
        if channel_id:
            channel = self.bot.get_channel(channel_id)
        else:
            for channel in member.guild.text_channels:
                if channel.permissions_for(member.guild.me).send_messages:
                    break

        if channel:  # Verificar si se encontró un canal
            leave_text = random.choice(self.leave_messages).format(mention=member.mention)
            leave_count = f"Total Cinammon Members turns down: {member.guild.member_count}"
            # Generar un color pastel aleatorio
            embed_color = self.generate_pastel_color()

            embed = discord.Embed(description=leave_text, color=embed_color)
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            embed.set_footer(text=f"Cinammon | Your Trusted Host! | {leave_count}")
            
            try:
                await channel.send(embed=embed)
            except Exception as e:
                print(f"Error al enviar mensaje de despedida: {e}")
        else:
            print("No se encontró un canal adecuado para enviar el mensaje de despedida.")
            
    @commands.command(name='setleave', aliases=['sleave'], help='Establece el canal de despedida para nuevos miembros.')
    @commands.has_permissions(administrator=True)
    async def set_leave_channel(self, ctx, channel: discord.TextChannel):
        self.leave_channels[ctx.guild.id] = channel.id 
        await ctx.send(f'El canal de despedida se ha establecido en: {channel.mention}')
        
    @commands.command(name='delleave', aliases=['dlleave'], help='Elimina el canal de despedida para nuevos miembros.')
    @commands.has_permissions(administrator=True)
    async def del_leave_channel(self, ctx):
        self.leave_channels.pop(ctx.guild.id)
        await ctx.send('El canal de despedida ha sido eliminado.')
 
async def setup(bot):
    await bot.add_cog(Leave(bot))
     
'''

