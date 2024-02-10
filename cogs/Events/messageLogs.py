import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logs_enabled = False
        self.color_pastel = 0xFFC0CB
        self.log_channel_id = None 

    @commands.command(name="setLogs", aliases=["sl"])
    async def setLogs(self, ctx, state: str, channel: discord.TextChannel = None):
        if state.lower() == "on":
            if channel:
                self.log_channel_id = channel.id
                self.logs_enabled = True
                await ctx.send(f"Los registros han sido activados. Los registros se enviarán al canal {channel.mention}.", delete_after=5)
            else:
                await ctx.send("Por favor, menciona el canal al que deseas enviar los registros.", delete_after=5)
                
        elif state.lower() == "off":
            self.logs_enabled = False
            await ctx.send("Los registros han sido desactivados.", delete_after=5)
        else:
            await ctx.send("Por favor, usa `on` o `off` para activar o desactivar los registros.", delete_after=5)
            await ctx.message.delete()

        # Eliminar el mensaje del usuario
        await ctx.message.delete()

    async def send_log_embed(self, embed):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            await channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description=f"warning: Could not find the channel for notifications. Make sure the channel ID is correct.",
                color=self.color_pastel
            )
            await self.bot.get_channel(self.log_channel_id).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(channel, self):
        if not channel.guild:
            return
        if not self.logs_enabled:
            return
        embed = discord.Embed(
            title="Canal creado",
            description=f"El canal {channel.mention} ha sido creado.",
            color=self.color_pastel
        )

async def setup(bot):
    await bot.add_cog(Logging(bot))
