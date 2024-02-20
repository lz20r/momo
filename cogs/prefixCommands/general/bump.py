import discord
from discord.ext import commands
import time

class BumpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bump_cooldowns = {}

    @commands.command(name='bump')
    async def bump(self, ctx, invite_link: str = None):
        user_id = ctx.author.id
        if not invite_link:
            await ctx.send("Por favor, proporciona un enlace de invitación.")
            return

        # Verificar si el enlace parece válido (esto es muy básico, podría ser más complejo)
        if "discord.gg/" not in invite_link and "discord.com/invite/" not in invite_link:
            await ctx.send("Eso no parece ser un enlace de invitación válido de Discord.")
            return

        if user_id in self.bump_cooldowns and (time.time() - self.bump_cooldowns[user_id]) < 180:
            time_left = 180 - (time.time() - self.bump_cooldowns[user_id])
            await ctx.send(f"{ctx.author.mention}, debes esperar {int(time_left)} segundos antes de poder hacer otro bump.", delete_after=10)
            await ctx.message.delete()
        else:
            self.bump_cooldowns[user_id] = time.time()

            embed = discord.Embed(title="¡Unete a nuestro servidor!", description="¡Haz clic abajo para unirte ahora y no te pierdas de nada!", color=discord.Color.green())
            embed.add_field(name="Invitación al servidor", value=f"[Haz clic aquí para unirte]({invite_link})", inline=False)
            embed.set_footer(text="Compartido por " + ctx.author.display_name)

            await ctx.send(embed=embed)
            await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(BumpCommands(bot))