import discord
from discord.ext import commands
from discord.ui import Select, View, Button, button

class Purgar(commands.Cog):
   """Recieves ping commands"""
 
   def __init__(self, bot):
      self.bot = bot   
  

   @commands.command(name="purge", aliases=['cls','purg', 'pur', 'cl', 'clear'])
   @commands.has_permissions(manage_messages=True) 
   async def clear(self, ctx: commands.Context, amount: int = None): 
    try: 
        await ctx.message.delete()
        if amount is None:
            embed = discord.Embed( 
            description=
            f"<:mtinfo:1205861978594091109> **Executing** `{ctx.command.qualified_name}` command\n\n"
            f"**This command can delete a certain amount of messages sent on that channel**\n```Syntax: momoclear  <number message>\nExample: momoclear 100```")
            await ctx.send(embed=embed, delete_after=10)
            return
        if isinstance(ctx.channel, discord.Thread):
            messages_deleted = 0
            async for message in ctx.channel.history(limit=amount):
                try:
                    await message.delete()
                    messages_deleted += 1
                except discord.Forbidden:
                    print(f"Unable to delete message {message.id}")
                
                embed = discord.Embed(
                description=
                f"<:mtinfo:1205861978594091109> **Executing** `{ctx.command.qualified_name}` command\n\n"
                f"{ctx.command.qualified_name} **{messages_deleted}** messages.")
                return await ctx.send(embed=embed, delete_after=10)    
            else :
                await ctx.message.delete()
                deleted_messages = await ctx.channel.purge(limit=amount)
                embed = discord.Embed(title="", description=f"purge **{len(deleted_messages)}** messages.")
                await ctx.send(embed=embed, delete_after=10)
    
        if isinstance(ctx.channel, discord.Thread):
            messages_deleted = 0
            async for message in ctx.channel.history(limit=amount):
                try:
                    await message.delete()
                    messages_deleted += 1
                except discord.Forbidden:
                    print(f"Unable to delete message {message.id}")
                
                embed = discord.Embed(
                description=
                f"<:mtinfo:1205861978594091109> **Executing** `{ctx.command.qualified_name}` command\n\n"
                f"{ctx.command.qualified_name} **{messages_deleted}** messages.")
                return await ctx.send(embed=embed, delete_after=10)    
            else :
                await ctx.message.delete()
                deleted_messages = await ctx.channel.purge(limit=amount)
                embed = discord.Embed(title="", description=f"purge **{len(deleted_messages)}** messages.")
                await ctx.send(embed=embed, delete_after=10)
        
        deleted_messages = await ctx.channel.purge(limit=amount)

        embed = discord.Embed(
            description=
            f"<:mtinfo:1205861978594091109> **Executing** `{ctx.command.qualified_name}` command\n\n"
            f"{ctx.author.mention} Deleted **{len(deleted_messages)}** messages.")
        return await ctx.send(embed=embed, delete_after=5)
    
    except:
        embed = discord.Embed(
           description=
           f"<:kerror:1196112444246995026> **Something went wrong.**"
        )
        return await ctx.send(embed=embed, delete_after=5)
    
async def setup(bot):
   await bot.add_cog(Purgar(bot)) 

 