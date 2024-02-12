import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logs_enabled = False
        self.color_pastel = 0xFFC0CB
        self.log_channel_id = 1202160434686201896    

    @commands.command(name="setLogs", aliases=["sl"])
    async def setLogs(self, ctx, state: str):
        if state.lower() == "on":
            self.logs_enabled = True
            await ctx.send("Los registros han sido activados.", delete_after=5)
        elif state.lower() == "off":
            self.logs_enabled = False
            await ctx.send("Los registros han sido desactivados.", delete_after=5)
        else:
            await ctx.send("Por favor, usa `on` o `off` para activar o desactivar los registros.", delete_after=5)
            await ctx.message.delete()

    async def send_log_embed(self, embed):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return 
        if message.author.bot == self.bot.user.bot:
            return
        if message.author == message.guild.me:
            return
        if self.logs_enabled:
            embed = discord.Embed(
                title="New Message",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=message.guild.name)
            embed.add_field(name="Canal", value=message.channel.mention)
            embed.add_field(name="User", value=message.author.mention)
            embed.add_field(name="Message", value=message.content)
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
            embed.set_footer(text=f"ID: {message.id}")
            await self.send_log_embed(embed)
      
      
    @commands.Cog.listener() 
    async def on_voice_state_update(self, member, before, after):
        if self.logs_enabled:
            if before.channel is None and after.channel is not None:
                embed = discord.Embed(
                    title="Voice Channel Joined",
                    color=self.color_pastel
                )
                embed.add_field(name="Server", value=member.guild.name)
                embed.add_field(name="Voice Channel", value=after.channel.name)
                embed.add_field(name="User", value=member.mention)
                embed.add_field(name="Message", value="None")
                embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
                embed.set_footer(text=f"ID: {member.id}")
                await self.send_log_embed(embed)
                
            if before.channel is not None and after.channel is None:
                embed = discord.Embed(
                    title="Voice Channel Left",
                    color=self.color_pastel
                )
                embed.add_field(name="Server", value=member.guild.name)
                embed.add_field(name="Voice Channel", value="None")
                embed.add_field(name="User", value=member.mention)
                embed.add_field(name="Message", value="None")
                embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
                embed.set_footer(text=f"ID: {member.id}")
                await self.send_log_embed(embed)
                
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        if self.logs_enabled:
            embed = discord.Embed(
                title="Message Deleted",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=message.guild.name)
            embed.add_field(name="Canal", value=message.channel.mention)
            embed.add_field(name="User", value=message.author.mention)
            embed.add_field(name="Message", value=message.content)
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
            embed.set_footer(text=f"ID: {message.id}")
            await self.send_log_embed(embed)
            
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return
        if self.logs_enabled:
            embed = discord.Embed(
                title="Message Edited",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=before.guild.name)
            embed.add_field(name="Canal", value=before.channel.mention)
            embed.add_field(name="User", value=before.author.mention)
            embed.add_field(name="Before", value=before.content)
            embed.add_field(name="After", value=after.content)
            embed.set_author(name=before.author.display_name, icon_url=before.author.display_avatar.url)
            embed.set_footer(text=f"ID: {before.id}")
            await self.send_log_embed(embed)
            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.logs_enabled:
            embed = discord.Embed(
                title="Member Joined",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=member.guild.name)
            embed.add_field(name="User", value=member.mention)
            embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
            embed.set_footer(text=f"ID: {member.id}")
            await self.send_log_embed(embed)
            
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.logs_enabled:
            embed = discord.Embed(
                title="Member Left",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=member.guild.name)
            embed.add_field(name="User", value=member.mention)
            embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
            embed.set_footer(text=f"ID: {member.id}")
            await self.send_log_embed(embed)
            
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if self.logs_enabled:
            if before.nick != after.nick:
                embed = discord.Embed(
                    title="Nickname Changed",
                    color=self.color_pastel
                )
                embed.add_field(name="Server", value=before.guild.name)
                embed.add_field(name="User", value=before.mention)
                embed.add_field(name="Before", value=before.nick)
                embed.add_field(name="After", value=after.nick)
                embed.set_author(name=before.display_name, icon_url=before.display_avatar.url)
                embed.set_footer(text=f"ID: {before.id}")
                await self.send_log_embed(embed)
                
            if before.roles != after.roles:
                embed = discord.Embed(
                    title="Role Changed",
                    color=self.color_pastel
                )
                embed.add_field(name="Server", value=before.guild.name)
                embed.add_field(name="User", value=before.mention)
                embed.add_field(name="Before", value=before.roles)
                embed.add_field(name="After", value=after.roles)
                embed.set_author(name=before.display_name, icon_url=before.display_avatar.url)
                embed.set_footer(text=f"ID: {before.id}")
                await self.send_log_embed(embed)
                
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if self.logs_enabled:
            embed = discord.Embed(
                title="Role Created",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=role.guild.name)
            embed.add_field(name="Role", value=role.mention)
            embed.set_author(name=role.name, icon_url=role.guild.icon.url)
            embed.set_footer(text=f"ID: {role.id}")
            await self.send_log_embed(embed)
            
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if self.logs_enabled:
            embed = discord.Embed(
                title="Role Deleted",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=role.guild.name)
            embed.add_field(name="Role", value=role.mention)
            embed.set_author(name=role.name, icon_url=role.guild.icon.url)
            embed.set_footer(text=f"ID: {role.id}")
            await self.send_log_embed(embed)
            
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if self.logs_enabled:
            embed = discord.Embed(
                title="Role Updated",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=before.guild.name)
            embed.add_field(name="Role", value=before.mention)
            embed.add_field(name="Before", value=before.roles)
            embed.add_field(name="After", value=after.roles)
            embed.set_author(name=before.name, icon_url=before.guild.icon.url)
            embed.set_footer(text=f"ID: {before.id}")
            await self.send_log_embed(embed)
            
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if self.logs_enabled:
            embed = discord.Embed(
                title="User Banned",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=guild.name)
            embed.add_field(name="User", value=user.mention)
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            embed.set_footer(text=f"ID: {user.id}")
            await self.send_log_embed(embed)
            
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if self.logs_enabled:
            embed = discord.Embed(
                title="User Unbanned",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=guild.name)
            embed.add_field(name="User", value=user.mention)
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            embed.set_footer(text=f"ID: {user.id}")
            await self.send_log_embed(embed)
     
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        if self.logs_enabled:
            embed = discord.Embed(
                title=f"Bulk Message Deleted",
                color=self.color_pastel
            )
            embed.add_field(name="Server", value=messages[0].guild.name)
            embed.add_field(name="Messages", value=len(messages))
            embed.set_author(name=messages[0].author.display_name, icon_url=messages[0].author.display_avatar.url)
            embed.set_footer(text=f"ID: {messages[0].id}")
            await self.send_log_embed(embed)
    
    @commands.Cog.listener()
    async def restart(self):
        if self.logs_enabled:
            embed = discord.Embed(
                title="Restarted",
                color=self.color_pastel
            )
            await self.send_log_embed(embed)
            
    @commands.Cog.listener()
    async def shutdown(self):
        if self.logs_enabled:
            embed = discord.Embed(
                title="Shutdown",
                color=self.color_pastel
            )
            await self.send_log_embed(embed)
             
async def setup(bot):
    await bot.add_cog(Logging(bot))
