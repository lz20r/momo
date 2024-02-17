import discord
import difflib
import inspect
import random
from discord.ext import commands 
from discord.ext.commands import CommandNotFound

class CommandsError(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error): 
        """Log command errors"""
        embed_color = random_pastel()
        if isinstance(error, commands.MissingPermissions):
            command_name = ctx.command.name
            embed = discord.Embed(title="", description=f"<a:MT_warning:1208184660987875378> You are not allowed to use the `{command_name}` command, {ctx.author.mention}!", color=embed_color)
            await ctx.send(embed=embed, delete_after=20)
        elif isinstance(error, commands.BotMissingPermissions):
            command_name = ctx.command.name
            embed = discord.Embed(title="", description=f"<a:MT_warning:1208184660987875378> I am not allowed to use the `{command_name}` command, {ctx.author.mention}!", color=embed_color)
            await ctx.send(embed=embed, delete_after=20)       
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(description=f"<a:MT_warning:1208184660987875378> User not found on this server, {ctx.author.mention}!", color=embed_color)
            await ctx.send(embed=embed, delete_after=20)
        elif isinstance(error, commands.CommandNotFound):  
            command_name = ctx.invoked_with
            available_commands = [command.name for command in self.bot.commands]
            closest_command = difflib.get_close_matches(command_name, available_commands, n=1)
            if closest_command:
                suggestion = closest_command[0]
                embed = discord.Embed(description=f"<a:MT_warning:1208184660987875378> Command `{command_name}` not found, try **{suggestion}**, {ctx.author.mention}!", color=embed_color)
            else:
                embed = discord.Embed(description=f"<a:MT_warning:1208184660987875378> Command `{command_name}` not found, {ctx.author.mention}!", color=embed_color)          
            await ctx.send(embed=embed, delete_after=20)
        elif isinstance(error, discord.errors.HTTPException):
            error_message = str(error)
            if 'Invalid Form Body In embeds.0.description: This field is required' in error_message:
                embed = discord.Embed(description="<a:MT_warning:1208184660987875378> HTTPException - Invalid Form Body, {ctx.author.mention}!", color=embed_color)
                await ctx.send(embed=embed, delete_after=20)
            else:
                embed = discord.Embed(description=f"<a:MT_warning:1208184660987875378> An error has occurred, {ctx.author.mention}!", color=embed_color)
                await ctx.send(embed=embed, delete_after=20)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(description=f"<a:MT_warning:1208184660987875378> You do not have permission to use this command, {ctx.author.mention}!", color=embed_color)
            await ctx.send(embed=embed, delete_after=20)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(description=f"<a:MT_warning:1208184660987875378> This command is on cooldown. Please try again in {error.retry_after:.2f} seconds, {ctx.author.mention}!", color=embed_color)
            await ctx.send(embed=embed, delete_after=20)
        else:
            # Get the line number where the error occurred
            error_line = inspect.currentframe().f_back.f_lineno
            embed = discord.Embed(description=f"<a:MT_warning:1208184660987875378> **Error at line {error_line}** executing `{ctx.command.qualified_name}` by {ctx.author.mention} ```{error}```", color=embed_color)
            await ctx.send(embed=embed, delete_after=120) 

async def setup(bot):
    await bot.add_cog(CommandsError(bot))  

def random_pastel():
    """Generate a random pastel color."""
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return discord.Color.from_rgb(r, g, b)
