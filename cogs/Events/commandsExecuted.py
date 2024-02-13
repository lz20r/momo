import discord
from discord.ext import commands

class logs(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        channel_id = 1206515724848332830
        target_channel = self.bot.get_channel(channel_id)

        if target_channel:
            command_name = ctx.command.name
            author_name = ctx.author.mention
            author_name_id = ctx.author.id
            server_name = ctx.guild.name if ctx.guild else 'Direct Message'
            channel_name = ctx.channel.mention if ctx.guild else 'Direct Message'

            user_prefix = await self.bot.get_prefix(ctx.message)

            embed = discord.Embed(
                title=f'`Command Executed`',
                description=f'Server: **{server_name}**\nChannel: **{channel_name}**\nUser: **{author_name}**\nUser ID: **{author_name_id}**\nCommand: **{command_name}**\nPrefix: **{user_prefix}**')
            await target_channel.send(embed=embed)  

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        channel_id = 1204154596864565259
        channel = self.bot.get_channel(channel_id)
        if channel:
            command_name = ctx.command.name
            author_name = ctx.author.mention
            author_name_id = ctx.author.id
            server_name = ctx.guild.name if ctx.guild else 'Direct Message'
            channel_name = ctx.channel.mention if ctx.guild else 'Direct Message'

            user_prefix = await self.bot.get_prefix(ctx.message)
 
            embed = discord.Embed(
                title=f'`Command Executed`',
                description=f'Server: **{server_name}**\nChannel: **{channel_name}**\nUser: **{author_name}**\nUser ID: **{author_name_id}**\nCommand: **{command_name}**\nPrefix: **{user_prefix}**')
            await channel.send(embed=embed)  

async def setup(bot):
    await bot.add_cog(logs(bot))
