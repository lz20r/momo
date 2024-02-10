import discord
from discord.ext import commands

class Silence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command("silence" , aliases=["s"])
    @commands.has_permissions(administrator=True)
    async def silence(self, ctx, member: discord.Member, *, reason=None):
        await member.move_to(None, reason=reason)
        await ctx.send(f"{member.mention} ha sido silenciado.")
        await member.send(f"Has sido silenciado por {ctx.author} por la razón: {reason}")
        await ctx.send(f"{ctx.author.mention} ha silenciado a {member.mention}.")
        
    @commands.command("unsilence", aliases=["us"])
    @commands.has_permissions(administrator=True)
    async def unsilence(self, ctx, member: discord.Member):
        await member.move_to(None)
        await ctx.send(f"{member.mention} ha sido desilenciado.")
        await ctx.send(f"{ctx.author.mention} ha desilenciado a {member.mention}.")
        await member.send(f"Has sido desilenciado por {ctx.author}.")
        
    @commands.command("silenced", aliases=["ss"])
    @commands.has_permissions(administrator=True)
    async def silenced(self, ctx):
        for member in ctx.guild.members:
            if member.voice and member.voice.channel:
                await member.move_to(None)
        await ctx.send("Todos los miembros han sido silenciados.")
        await ctx.send(f"{ctx.author.mention} ha silenciado todos los miembros.")
        await ctx.send(f"{ctx.author.mention} ha desilenciado todos los miembros.")
        
    @commands.command("unsilenced", aliases=["uss"])
    @commands.has_permissions(administrator=True)
    async def unsilenced(self, ctx):
        for member in ctx.guild.members:
            if member.voice and member.voice.channel:
                await member.move_to(None)
        await ctx.send("Todos los miembros han sido desilenciados.")
        await ctx.send(f"{ctx.author.mention} ha desilenciado todos los miembros.")
        
async def setup(bot):
    await bot.add_cog(Silence(bot))
