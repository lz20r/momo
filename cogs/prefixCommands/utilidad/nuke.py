import discord
from discord.ext import commands
import asyncio

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        """Nukes all messages in the specified channel. Requires Manage Channels permission."""
        if channel is None:
            channel = ctx.channel

        # Confirm nuke operation
        confirmation = await ctx.send(f"Are you sure you want to nuke {channel.mention}? Type 'yes' to confirm.")
        def check(m):
            return m.author == ctx.author and m.content.lower() == "yes"

        try:
            await self.bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send('Nuke operation cancelled.', delete_after=1)
            return

        # Clone the channel (creates a copy with the same permissions and name)
        new_channel = await channel.clone(reason="Nuke command used")
        # Delete the old channel
        await channel.delete(reason="Nuke command used") 
        await new_channel.send("Channel has been nuked!", delete_after=1)
 
async def setup(bot):
    await bot.add_cog(Nuke(bot))
