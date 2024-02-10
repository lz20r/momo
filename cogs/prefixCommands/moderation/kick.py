import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command('kick' , aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            # Crea un embed para el mensaje de confirmación
            embed = discord.Embed(title="Miembro Expulsado", description=f"{member.mention} ha sido expulsado.", color=discord.Color.blue())
            embed.add_field(name="Razón", value=reason, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"No fue posible expulsar a {member.mention}. Error: {e}")
        
async def setup(bot):
    await bot.add_cog(Moderation(bot))
