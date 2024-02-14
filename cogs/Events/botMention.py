import discord
from discord.ext import commands

class Mention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(self.bot.user.mention):
            prefix = await self.bot.get_prefix(message)
            embed_hello = discord.Embed(description=f"<a:MT_Penguin:1207211476331528192>hii little momos mu actual prefix is `{prefix}`")
            await message.reply(embed=embed_hello)

async def setup(bot):
    await bot.add_cog(Mention(bot))