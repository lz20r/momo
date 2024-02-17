import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='kick' , aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            # Crea un embed para el mensaje de confirmación
            embed = discord.Embed(title="Miembro Expulsado", description=f"{member.mention} ha sido expulsado.", color=discord.Color.blue())
            embed.add_field(name="Razón", value=reason, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"No fue posible expulsar a {member.mention}. Error: {e}")

    @commands.command(name='unkick', aliases=['uk'])
    @commands.has_permissions(kick_members=True)
    async def unkick(self, ctx, member: discord.Member):
        try:
            await member.kick()
            await ctx.send(f"{member.mention} ha sido desexpulsado.")
        except Exception as e:
            await ctx.send(f"No fue posible desexpulsar a {member.mention}. Error: {e}")
            
async def setup(bot):
    await bot.add_cog(Kick(bot)) 
