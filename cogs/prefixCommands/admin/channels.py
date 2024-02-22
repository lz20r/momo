import discord
from discord.ext import commands
import random

def pastel_color():
    r = random.randint(180, 255)
    g = random.randint(180, 255)
    b = random.randint(180, 255)
    return discord.Color.from_rgb(r, g, b)

class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel_id = 1207414274717392926  # ID of the channel where you want to send success messages
        self.error_channel_id = 1207414274717392926  # ID of the channel where you want to send error messages

    async def send_embed_message(self, message, channel_id, color=pastel_color):
        channel = self.bot.get_channel(channel_id)
        embed = discord.Embed(title=f"{self.bot.user} Channel and Thread Management", description=message, color=color())
        await channel.send(embed=embed)

    async def send_error_message(self, error_message):
        channel = self.bot.get_channel(self.error_channel_id)
        embed = discord.Embed(
            title="Error",
            description=str(error_message),
            color=discord.Color.red()
        )
        await channel.send(embed=embed)

    @commands.command(name="CreateChannel", aliases=["CCH", "CrCh", "Cchannel"])
    @commands.has_permissions(administrator=True)    
    async def create_channel(self, ctx, channel_name):
        guild = ctx.guild
        try:
            await guild.create_text_channel(channel_name)
            message = f"The channel {channel_name} in category {guild.categories[0].name} has been created in {guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except discord.Forbidden:
            await self.handle_forbidden_error()
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="DeleteChannel", aliases=["DCH", "DCh", "Dchannel"])
    @commands.has_permissions(administrator=True)
    async def delete_channel(self, ctx, channel: discord.TextChannel):
        try:
            await channel.delete()
            message = f"The channel {channel.name} in category {channel.category.name} has been deleted in {channel.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="UpdateChannel", aliases=["UCH", "UCh", "UChannel"])
    @commands.has_permissions(administrator=True)
    async def update_channel(self, ctx, channel: discord.TextChannel, new_name):
        try:
            await channel.edit(name=new_name)
            message = f"The channel {channel.name} in category {channel.category.name} has been updated to {new_name} in {channel} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="RenameChannel", aliases=["RCH", "RCh", "Rchannel"])
    @commands.has_permissions(administrator=True)
    async def rename_channel(self, ctx, channel: discord.TextChannel, new_name):
        try:
            await channel.edit(name=new_name)
            message = f"The channel {channel.name} in category {channel.category.name} has been renamed to {new_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="CreateThread", aliases=["CrTh", "CTh", "Cthread"])
    @commands.has_permissions(administrator=True)
    async def create_thread(self, ctx, thread_name, channel: discord.TextChannel = None):
        try:
            await ctx.channel.create_thread(name=thread_name)
            message = f"The thread {thread_name} has been created in {ctx.channel.name} in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="DeleteThread", aliases=["DlTh", "DTh", "Dthread"])
    @commands.has_permissions(administrator=True)
    async def delete_thread(self, ctx, thread: discord.Thread):
        try:
            await thread.delete()
            message = f"The thread {thread.name} in {ctx.channel.name} has been deleted in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="UpdateThread", aliases=["UpTh", "UTh", "Uthread"])
    @commands.has_permissions(administrator=True)
    async def update_thread(self, ctx, thread: discord.Thread, new_name):
        try:
            await thread.edit(name=new_name)
            message = f"The thread {thread.name} in {ctx.channel.name} has been updated to {new_name} in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="RenameThread", aliases=["RnTh", "RTh", "Rthread"])
    @commands.has_permissions(administrator=True)
    async def rename_thread(self, ctx, thread: discord.Thread, new_name):
        try:
            await thread.edit(name=new_name)
            message = f"The thread {thread.name} in {ctx.channel.name} has been renamed to {new_name} in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)

    @commands.command(name="ArchiveThread", aliases=["ArTh", "ATh", "Arthread"])
    @commands.has_permissions(administrator=True)
    async def archive_thread(self, ctx, thread: discord.Thread):
        try:
            await thread.edit(archived=True)
            message = f"The thread {thread.name} in {ctx.channel.name} has been archived in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="UnarchiveThread", aliases=["UnArTh", "UnATh", "UnArthread"])
    @commands.has_permissions(administrator=True)
    async def unarchive_thread(self, ctx, thread: discord.Thread):
        try:
            await thread.edit(archived=False)
            message = f"The thread {thread.name} in {ctx.channel.name} has been unarchived in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="LockThread", aliases=["LkTh", "LTh", "Lthread"])
    @commands.has_permissions(administrator=True)
    async def lock_thread(self, ctx, thread: discord.Thread):
        try:
            await thread.edit(locked=True)
            message = f"The thread {thread.name} in {ctx.channel.name} has been locked in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="UnlockThread", aliases=["UnLkTh", "UnLTh", "UnLthread"])
    @commands.has_permissions(administrator=True)
    async def unlock_thread(self, ctx, thread: discord.Thread):
        try:
            await thread.edit(locked=False)
            message = f"The thread {thread.name} in {ctx.channel.name} has been unlocked in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="PinMessage", aliases=["Pin", "PinM", "PinMess", "Pingmsg"])
    @commands.has_permissions(administrator=True)
    async def pin_message(self, ctx, message: discord.Message):
        try:
            await message.pin()
            message = f"The message {message.id} in {ctx.channel.name} has been pinned in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="UnpinMessage", aliases=["Unpin", "UnpinM", "UnpinMess", "Unpingmsg"])
    @commands.has_permissions(administrator=True)
    async def unpin_message(self, ctx, message: discord.Message):
        try:
            await message.unpin()
            message = f"The message {message.id} in {ctx.channel.name} has been unpinned in {ctx.channel.category} in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="CreateCategory", aliases=["CrCat", "CCat", "Ccat"])
    @commands.has_permissions(administrator=True)
    async def create_category(self, ctx, category_name):
        try:
            await ctx.guild.create_category(name=category_name)
            message = f"The category {category_name} has been created in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="DeleteCategory", aliases=["DlCat", "DCat", "Dcat"])
    @commands.has_permissions(administrator=True)
    async def delete_category(self, ctx, category: discord.CategoryChannel):
        try:
            await category.delete()
            message = f"The category {category.name} has been deleted in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="UpdateCategory", aliases=["UpCat", "UCat", "Ucat"])
    @commands.has_permissions(administrator=True)
    async def update_category(self, ctx, category: discord.CategoryChannel, new_name):
        try:
            await category.edit(name=new_name)
            message = f"The category {category.name} has been updated in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="RenameCategory", aliases=["RnCat", "RCat", "Rcat"])
    @commands.has_permissions(administrator=True)
    async def rename_category(self, ctx, category: discord.CategoryChannel, new_name):
        try:
            await category.edit(name=new_name)
            message = f"The category {category.name} has been renamed in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="CreateVoiceChannel", aliases=["CrVC", "CVc", "Cvc"])
    @commands.has_permissions(administrator=True)
    async def create_voice_channel(self, ctx, channel_name):
        try:
            await ctx.guild.create_voice_channel(channel_name)
            message = f"The voice channel {channel_name} has been created in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="DeleteVoiceChannel", aliases=["DlVC", "DVc", "Dvc"])
    @commands.has_permissions(administrator=True)
    async def delete_voice_channel(self, ctx, channel: discord.VoiceChannel):
        try:
            await channel.delete()
            message = f"The voice channel {channel.name} has been deleted in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="UpdateVoiceChannel", aliases=["UpVC", "UVc", "Uvc"])
    @commands.has_permissions(administrator=True)
    async def update_voice_channel(self, ctx, channel: discord.VoiceChannel, new_name):
        try:
            await channel.edit(name=new_name)
            message = f"The voice channel {channel.name} has been updated in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="RenameVoiceChannel", aliases=["RnVC", "RVc", "Rvc"])
    @commands.has_permissions(administrator=True)
    async def rename_voice_channel(self, ctx, channel: discord.VoiceChannel, new_name):
        try:
            await channel.edit(name=new_name)
            message = f"The voice channel {channel.name} has been renamed in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="CreateStageChannel", aliases=["CrSC", "CSc", "Csc"])
    @commands.has_permissions(administrator=True)
    async def create_stage_channel(self, ctx, channel_name):
        try:
            await ctx.guild.create_stage_channel(channel_name)
            message = f"The stage channel {channel_name} has been created in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="DeleteStageChannel", aliases=["DlSC", "DSc", "Dsc"])
    @commands.has_permissions(administrator=True)
    async def delete_stage_channel(self, ctx, channel: discord.StageChannel):
        try:
            await channel.delete()
            message = f"The stage channel {channel.name} has been deleted in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="UpdateStageChannel", aliases=["UpSC", "USc", "Usc"])
    @commands.has_permissions(administrator=True)
    async def update_stage_channel(self, ctx, channel: discord.StageChannel, new_name):
        try:
            await channel.edit(name=new_name)
            message = f"The stage channel {channel.name} has been updated in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
            
    @commands.command(name="RenameStageChannel", aliases=["RnSC", "RSc", "Rsc"])
    @commands.has_permissions(administrator=True)
    async def rename_stage_channel(self, ctx, channel: discord.StageChannel, new_name):
        try:
            await channel.edit(name=new_name)
            message = f"The stage channel {channel.name} has been renamed in {ctx.guild.name} by {ctx.author.display_name}."
            await self.send_embed_message(message, self.target_channel_id)
        except Exception as e:
            await self.send_error_message(e)
async def setup(bot):
    await bot.add_cog(Channels(bot))
