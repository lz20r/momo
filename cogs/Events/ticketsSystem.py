import discord
from discord.ext import commands 

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mysql_connection = bot.mysql_connection
        self.cursor = self.mysql_connection.cursor() 
        
    
    @commands.command(name="ticket")
    async def ticket(self, ctx):
        async def create_ticket(): 
            channel = await ctx.guild.create_text_channel("ticket " + ctx.author.name, category=ctx.channel.category)
            await channel.set_permissions(ctx.author, view_channel=True, send_messages=True)
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
            await channel.set_permissions(ctx.guild.me, view_channel=True, send_messages=True)
 
            embed = discord.Embed(description=f"{ctx.author.mention} Bienvenido a tu ticket.")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await channel.send(embed=embed)
            embed = discord.Embed(description=f"Ticket creado en {channel.mention}.")
            await ctx.send(embed=embed)
            return channel
        
        if ctx.channel.name == "ticket":
            await ctx.send("Ya tienes un ticket abierto.", delete_after=5)
        else:
            channel = await create_ticket()
            await ctx.author.move_to(channel)
            await ctx.message.delete()
            
    @commands.command(name="close")
    async def close(self, ctx):
        await ctx.channel.delete()
        await ctx.send("Ticket cerrado.")
        return
     
async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
