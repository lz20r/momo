import discord
from discord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        total_members = len(guild.members)
        total_bots = sum(1 for member in guild.members if member.bot)
        total_text_channels = len(guild.text_channels)
        total_voice_channels = len(guild.voice_channels)
        total_categories = len(guild.categories)
        total_roles = len(guild.roles)
        total_online_members = sum(1 for member in guild.members if member.status == discord.Status.online)
        total_text_online = sum(1 for channel in guild.text_channels if any(member.status == discord.Status.online for member in channel.members))
        total_voice_online = sum(1 for channel in guild.voice_channels if any(member.status == discord.Status.online for member in channel.members))

        embed = discord.Embed(title=f"Server Information: {guild.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="ID:", value=guild.id, inline=False)
        embed.add_field(name="Owner:", value=guild.owner, inline=False)
        embed.add_field(name="Region:", value=guild.region, inline=False)
        embed.add_field(name="Members:", value=f"Total: {total_members} 👥\nBots: {total_bots} 🤖\nOnline: {total_online_members} 🟢", inline=False)
        embed.add_field(name="Text Channels:", value=f"Total: {total_text_channels} 📝\nOnline: {total_text_online} 🟢", inline=False)
        embed.add_field(name="Voice Channels:", value=f"Total: {total_voice_channels} 🔊\nOnline: {total_voice_online} 🟢", inline=False)
        embed.add_field(name="Categories:", value=f"{total_categories} 🗂️", inline=False)
        embed.add_field(name="Roles:", value=f"{total_roles} 🛡️", inline=False)
        embed.add_field(name="Created At:", value=guild.created_at.strftime("%d/%m/%Y"), inline=False)
        embed.set_footer(text="ℹ️ Emojis: 👥 = Members, 🤖 = Bots, 🟢 = Online, 📝 = Text Channels, 🔊 = Voice Channels, 🗂️ = Categories, 🛡️ = Roles")
        await ctx.send(embed=embed)

async def setup(bot):
   await bot.add_cog(ServerInfo(bot))