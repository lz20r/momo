import discord
from discord.ext import commands

class Share(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sharepin')
    async def share_pin(self, ctx, pinterest_pin_url: str):
        # Verificar si el enlace parece ser una URL válida de Pinterest
        if "pinterest.com/pin/" in pinterest_pin_url:
            embed = discord.Embed(title="Pinterest Pin", description="Echa un vistazo a este pin en Pinterest!", url=pinterest_pin_url, color=0xE60023)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Por favor, proporciona una URL válida de un pin de Pinterest.")

async def setup(bot):
    await bot.add_cog(Share(bot))