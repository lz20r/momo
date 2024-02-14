import os 
import discord
from ast import Try  
from discord.utils import get 
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ui import Select, View, Button, button
 
class HelpView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.select( 
        placeholder="Choose a command",
        options=[ 
            discord.SelectOption(label='home', value='0', description=f'momo Home Page', emoji='<:8_wngs:1200775867673104526>'),
            discord.SelectOption(label='admin', value='1', description=f'momo Admin Commands', emoji='<:00_bpentagram:1200775838094856304>'),            
            discord.SelectOption(label='setup', value='2', description=f'momo Setup Commands', emoji='<:Bbutterfly:1200775841282523156>'),
            discord.SelectOption(label='general', value='3', description=f'momo Everyone Commands', emoji='<a:zzaneutralstar4:1200775864242151436>'),
            discord.SelectOption(label='misc', value='4', description=f'momo Misc Commands', emoji='<:black_emodiamond:1200775844344377405>'),
            discord.SelectOption(label='premium', value='5', description=f'momo Premium Commands', emoji='<:1911cashbagblack:1194495648842661918>'),
        ] 
    )
    async def select_callback(self, interaction, select):           
        select.disabled = True
        selected_value = interaction.data["values"][0]
        momo = self.bot.user.name
        momoprefix = "m."
        momoguildprefix = await self.bot.get_prefix(interaction.message)
        thumbnail_url = self.bot.user.avatar.url        
        if selected_value == "0":
            thumbnail_url = self.bot.user.avatar.url
            embed = discord.Embed(
                title=f"{momo} Home Page", 
                description=f"""
                > Momo's predefined prefix is `{momoprefix}`.
                > You can use `{momoguildprefix}help <command>` to get more information about a command.
                > Welcome to [{momo}](https://discord.gg/ezfkXgekw7)! Here you can find all the commands and features that {momo} has to offer.
                ```bf\nSupport Server: https://discord.gg/ezfkXgekw7```
                """)
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_author(name=f"{self.bot.user.name}", icon_url=thumbnail_url)
            await interaction.response.edit_message(embed=embed)

        if selected_value == "1":
            thumbnail_url = self.bot.user.avatar.url
            embed = discord.Embed(
                title=f"{momo} admin", 
                description=f"```yaml\n```")
            embed.set_thumbnail(url=thumbnail_url)
            await interaction.response.edit_message(embed=embed)
            
        if selected_value == "2":
            thumbnail_url = self.bot.user.avatar.url
            embed = discord.Embed(
                title=f"{momo} setup <3", 
                description=f"```yaml\n```")
            embed.set_thumbnail(url=thumbnail_url)
            await interaction.response.edit_message(embed=embed)        

        if selected_value == "3":
            thumbnail_url = self.bot.user.avatar.url
            embed = discord.Embed(
                title=f"{momo} general <3", 
                description=f"```yaml\n```")
            embed.set_thumbnail(url=thumbnail_url)
            await interaction.response.edit_message(embed=embed)

        if selected_value == "4":
            thumbnail_url = self.bot.user.avatar.url
            embed = discord.Embed(
                title=f"{momo} misc <3", 
                description=f"```yaml\n```")
            embed.set_thumbnail(url=thumbnail_url)
            await interaction.response.edit_message(embed=embed)
 
        if selected_value == "6":
            thumbnail_url = self.bot.user.avatar.url
            embed = discord.Embed(
                title=f"{momo} premium <3", 
                description=f"```yaml\n```")
            embed.set_thumbnail(url=thumbnail_url)
            await interaction.response.edit_message(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h", "commands", "cmd", "helpme", "hlp"])
    async def help(self, ctx):
        momo = self.bot.user.name
        momoprefix = "m."
        momoguildprefix = await self.bot.get_prefix(ctx.message)
        momoguildname = ctx.guild.name
        thumbnail_url = self.bot.user.avatar.url
        embed = discord.Embed(
            title=f"{momo} Home Page",  
            description= 
            f""" 
            > <:Flechaheart:1203068677570830407> `{momo}`'s prefix is `{momoprefix}`.
            > <:Flechaheart:1203068677570830407> `{momoguildprefix}help <command>` to get more info about a command.
            > <:Flechaheart:1203068677570830407> `{momoguildprefix}invite` to invite {momo} to your server  [Momo Invite](https://discord.gg/ezfkXgekw7).
            > <:Flechaheart:1203068677570830407> `{momoguildprefix}support` to join the support server of {momo}. [Momo](https://discord.gg/ezfkXgekw7) 
            > <:Flechaheart:1203068677570830407> `{momoguildprefix}donate` to donate to {momo}. [Cinammon Donation](https://www.patreon.com/cinammon)
            > <:Flechaheart:1203068677570830407> `{momoguildprefix}dashboard` to access your dashboard: [Dashboard](https://cinammon.es/panel). 
            > <:Flechaheart:1203068677570830407> `{momoguildprefix}patreon` if you {momo} wanna you support {momo}? [Patreon](https://www.patreon.com/cinammon)
            > <:Flechaheart:1203068677570830407> `{momoguildprefix}hosting` make sure to join [Cinammon Hosting](https://discord.gg/ezfkXgekw7)
            > <:Flechaheart:1203068677570830407> `{momoguildprefix}guide` if you  need help with {momo}? check the guide: [Cinammon Guide](https://docs.cinammon.es) 
            ```bf\nSupport Server: https://discord.gg/ezfkXgekw7!```
            """ )
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_author(name=f"{self.bot.user.name}", icon_url=thumbnail_url)
        await ctx.reply(embed=embed, view=HelpView(self.bot))

async def setup(bot): 
   await bot.add_cog(Help(bot)) 
 
