import discord
import difflib
from requests import delete 
from discord.ext import commands 
from discord.ext.commands import CommandNotFound

class CommandsError(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error): 
        """Log command errors"""
        if isinstance(error, commands.MissingPermissions):
            command_name = ctx.command.name
            embed = discord.Embed(title="", description=f"<:mtinfo:1205861978594091109>  You are not allowed to use the `{command_name}` command!")
            await ctx.send(embed=embed, delete_after=20)
        elif isinstance(error, commands.BotMissingPermissions):
            command_name = ctx.command.name
            embed = discord.Embed(title="", description=f"<:mtinfo:1205861978594091109>  You are not allowed to use the `{command_name}` command!")
            await ctx.send(embed=embed, delete_after=20)       
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(description=f"<:mtinfo:1205861978594091109>  User not found on this server.")
            await ctx.send(embed=embed, delete_after=20)
        elif isinstance(error, commands.CommandNotFound):  
            command_name = ctx.invoked_with
            available_commands = [command.name for command in self.bot.commands]
            closest_command = difflib.get_close_matches(command_name, available_commands, n=1)
            if closest_command:
                suggestion = closest_command[0]
                embed = discord.Embed(description=f"<:mtinfo:1205861978594091109>  Command `{command_name}` not found, try **{suggestion}**")
            else:
                embed = discord.Embed(description=f"<:mtinfo:1205861978594091109>  Command `{command_name}` not found.")          
            await ctx.send(embed=embed, delete_after=20)
        elif isinstance(error, discord.errors.HTTPException):
            error_message = str(error)
            if 'Invalid Form Body In embeds.0.description: This field is required' in error_message:
                embed = discord.Embed(description="<:mtinfo:1205861978594091109>  HTTPException - Invalid Form Body.")
                ctx.send(embed=embed, delete_after=20)
            else:
                embed = discord.Embed(description=f"<:mtinfo:1205861978594091109>  An error has occurred.")
                ctx.send(embed=embed, delete_after=20)
        else:
            embed = discord.Embed(description=f"<:mtinfo:1205861978594091109>  **Error at executing** `{ctx.command.qualified_name}` ```{error}```")
            await ctx.send(embed=embed, delete_after=120) 

async def setup(bot):
    await bot.add_cog(CommandsError(bot))  
