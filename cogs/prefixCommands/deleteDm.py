import discord
from discord.ext import commands

class DeleteDm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deleteDM", aliases=[Ddm], help="Elimina los mensajes del bot en el DM con el usuario.")
    async def clear_dm(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            async for message in ctx.channel.history(limit=100):
                if message.author == self.bot.user:
                    await message.delete()
            await ctx.send("Mensajes del bot eliminados.", delete_after=5)
        else:
            await ctx.send("Este comando solo funciona en DMs.", delete_after=5)

def setup(bot):
    bot.add_cog(DeleteDm(bot))