import discord
from discord.ext import commands
import random

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_messages = [
            "Cinammon is a host for new members! Welcome {mention}!",
            "Cinammon can be your host and you will satisfy for our service. Welcome {mention}!",
            "Thank you for joining, Cinammon will be your trusted host! Welcome {mention}!",
            "[cinammon.es](https://cinammon.es/panel) is a host for new members! Welcome {mention}!",
            "Try to use [cinammon.es](https://cinammon.es/panel) as your host. Welcome {mention}!",
            "You need to host any panel. [cinammon.es](https://cinammon.es/panel) is your host. Welcome {mention}!",
            "Try once and you will never regret. Welcome {mention}!",
            "Tysm {mention} for trusting us. Cinammon is your host!",
            "Cinammon is your host. Welcome {mention}!",
        ]

    def generate_pastel_color(self):
        # Genera valores RGB altos y equilibrados para colores pastel
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
            for channel in member.guild.text_channels:
                if channel.permissions_for(member.guild.me).send_messages:
                    break

        welcome_text = random.choice(self.welcome_messages).format(mention=member.mention)
        
        # Genera un color pastel aleatorio
        embed_color = self.generate_pastel_color()

        embed = discord.Embed(description=welcome_text, color=embed_color)
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.set_footer(text="Cinammon | Your Trusted Host!")

        await channel.send(embed=embed)

    @commands.command(name='setwelcome', aliases=['swlcm'], help='Establece el canal de bienvenida para nuevos miembros.')
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        self.welcome_channels[ctx.guild.id] = channel.id
        await ctx.send(f'El canal de bienvenida se ha establecido en: {channel.mention}')

async def setup(bot):
    await bot.add_cog(Welcome(bot))
