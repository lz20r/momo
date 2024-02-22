from unicodedata import category
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
            
            if channel is None:
                await ctx.send("No se pudo crear el ticket.", delete_after=5)
                return
            elif ctx.channel == channel:
                await ctx.send("Ya tienes un ticket abierto.", delete_after=5)
                return
            else:
                embed = discord.Embed(description=f"{ctx.author.mention} Bienvenido a tu ticket.")
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                await channel.send(embed=embed)
                embed = discord.Embed(description=f"Ticket created in {channel.mention} in {ctx.channel.category}")
                await ctx.send(embed=embed)
                return channel      
        await ctx.message.delete() 
        await create_ticket()
        return 
    
    @commands.command(name="close")
    async def close_ticket(self, ctx):
        await ctx.channel.delete()
        await ctx.send(f"Ticket closed {ctx.author.mention}", delete_after=5)
        return
    
    @commands.command(name="closeall")
    async def close_all_tickets(self, ctx):
        for channel in ctx.guild.channels:
            if channel.name.startswith(f"ticket {ctx.author.name}"): 
                await channel.delete()
        return
    
    @commands.command(name="closecategory")
    async def close_category(self, ctx):
        for channel in ctx.guild.channels:
            if channel.category == ctx.channel.category:
                await channel.delete()
        return
    
    @commands.command(name="closeallcategory")
    async def close_all_category(self, ctx):
        for channel in ctx.guild.channels:
            if channel.category == ctx.channel.category:
                await channel.delete()
        return
    
    @commands.command(name="logsticket")
    async def logs_ticket(self, ctx):
        channel_id = 1210022535635410944
        target_channel = self.bot.get_channel(channel_id)
        if target_channel:
            embed = discord.Embed(
                title=f'`Ticket Logs`',
                description=f'User: **{ctx.author.mention}**\nTicket: **{ctx.channel.name}**\nCategory: **{ctx.channel.category}**')
            await target_channel.send(embed=embed)
        return
    
     
     
async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
