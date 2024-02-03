import discord
from discord.ext import commands

class ProfileSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", aliases=["av", "setavatar", "set_av", "setav", "set_avatar"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        avatar_url = member.avatar.url

        embed = discord.Embed(title=f"Avatar de {member.display_name}")
        embed.set_image(url=avatar_url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ProfileSettings(bot)) 
