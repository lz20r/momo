import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command('ban', aliases=['b'])
    @commands.has_permissions(ban_members=True)    
    async def ban(ctx, member: discord.Member, *, reason=None):
        # Intenta banear al miembro
        try:
            await member.ban(reason=reason)
            # Crea un embed para el mensaje de confirmación
            embed = discord.Embed(title="Miembro Baneado", description=f"{member.mention} ha sido baneado.", color=discord.Color.red())
            embed.add_field(name="Razón", value=reason, inline=False)
            # Envía el embed
            await ctx.send(embed=embed)
        except Exception as e:
            # En caso de error, envía un mensaje
            await ctx.send(f"No fue posible banear a {member.mention}. Error: {e}") 

  
    @commands.command('unban', aliases=['ub'])
    @commands.has_permissions(unban_members=True)
    async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} ha sido desbaneado.")
                return
            
        await ctx.send(f"{member} no ha sido baneado.")
        
async def setup(bot):
    await bot.add_cog(Ban(bot))
