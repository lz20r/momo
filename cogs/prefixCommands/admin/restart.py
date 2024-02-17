import asyncio
import discord
from discord.ext import commands 

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart", aliases=["reset", "r"])
    async def restart(self, ctx):
        allowed_ids = [298704465178001418, 1033160523044376616]
        author_id = ctx.author.id 
        author_name = ctx.author.name
        if author_id not in allowed_ids:
            embed = discord.Embed(title="", description="<:momoswarn:1206264545308450917> You are not allowed to use the **restart** command!")
            await ctx.send(embed=embed, delete_after=10)
            return await ctx.message.delete()
        
        try:
            embed = discord.Embed(description=f"<:momostarw:1206266007090364486> {author_name} is restarting Momo")
            await ctx.send(embed=embed, delete_after=10)
            
            # Cambiar el estado a "Reiniciando..."
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name=f"{self.bot.user.name} is getting Restarting by {author_name}..."))
            
            # Detener el bot
            await asyncio.sleep(10)  
            await self.bot.close()
            
            # Cambiar el estado a "Online"
            await self.bot.change_presence(status=discord.Status.idle)
            
            embed = discord.Embed(description=f"<:momostarw:1206266007090364486> {author_name} restarted {self.bot.user.name}")
            await ctx.send(embed=embed)
             
        except Exception as e:
            print("Error durante el reinicio:", e)

async def setup(bot):
    await bot.add_cog(Restart(bot))
