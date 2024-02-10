import discord
from discord.ext import commands

class MentionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(self.bot.user.mention):
            prefix = await self.bot.get_prefix(message)
            embed_hello = discord.Embed(title="", description=f"<:mtinfo1:1205311004066451507> my prefix here is `{prefix}`")
            await message.reply(embed=embed_hello)

async def setup(bot):
    await bot.add_cog(MentionCog(bot))