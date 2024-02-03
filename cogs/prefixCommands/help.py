from ast import Try
import os 
import discord
from discord.ext import commands
from discord.utils import get 
from discord.ext.commands import CommandNotFound
import discord as prefix
from discord.ui import Select, View, Button, button
 
class HelpView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.select(
        placeholder="Choose a command",
        options=[
            discord.SelectOption(label='Home', value='category1'),
            discord.SelectOption(label='Action', value='category2'),
            discord.SelectOption(label='Categoría 3', value='category3'),
            discord.SelectOption(label='Categoría 4', value='category4'),
            discord.SelectOption(label='Categoría 5', value='category5'),
            discord.SelectOption(label='Categoría 6', value='category6'),
            discord.SelectOption(label='Categoría 7', value='category7'),
            discord.SelectOption(label='Categoría 8', value='category8'),
            discord.SelectOption(label='Categoría 9', value='category9'),
            discord.SelectOption(label='Categoría 10', value='category10'),
            discord.SelectOption(label='Categoría 11', value='category11'),
            discord.SelectOption(label='Categoría 12', value='category12'),
            discord.SelectOption(label='Categoría 13', value='category13'),
            discord.SelectOption(label='Categoría 14', value='category14'),
            discord.SelectOption(label='Categoría 15', value='category15'),
            discord.SelectOption(label='Categoría 16', value='category16'),
            discord.SelectOption(label='Categoría 17', value='category17'),
        ] 
    )
    async def select_callback(self, interaction, select):  
        prefix = self.bot.command_prefix 
        if select.values[0] == 'category1':
            embed = discord.Embed(
                title="**Welcome to {} home page <3**".format(self.bot.user),
                description="{}".format(commands)
            )
            
            await interaction.response.edit_message(embed=embed)

        elif select.values[0] == 'category2':
            embed = discord.Embed(
                title="Action", 
                description=
                "Ayuda detallada sobre un comando: `{}help <action>`\n\n".format(prefix) 
            )
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category3':
            embed = discord.Embed(title="Categoría 3", description="This is the third category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category4':
            embed = discord.Embed(title="Categoría 4", description="This is the fourth category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category5':
            embed = discord.Embed(title="Categoría 5", description="This is the fifth category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category6':
            embed = discord.Embed(title="Categoría 6", description="This is the sixth category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category7':
            embed = discord.Embed(title="Categoría 7", description="This is the seventh category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category8':
            embed = discord.Embed(title="Categoría 8", description="This is the eighth category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category9':
            embed = discord.Embed(title="Categoría 9", description="This is the ninth category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category10':
            embed = discord.Embed(title="Categoría 10", description="This is the tenth category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category11':
            embed = discord.Embed(title="Categoría 11", description="This is the eleventh category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category12':
            embed = discord.Embed(title="Categoría 12", description="This is the twelfth category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category13':
            embed = discord.Embed(title="Categoría 13", description="This is the thirteenth category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category14':
            embed = discord.Embed(title="Categoría 14", description="This is the fourteenth category")
            await interaction.response.edit_message(embed=embed)


        elif select.values[0] == 'category15':
            embed = discord.Embed(title="Categoría 15", description="This is the fifteenth category")
            await interaction.response.edit_message(embed=embed)

        elif select.values[0] == 'category16':
            embed = discord.Embed(title="Categoría 16", description="This is the sixteenth category")
            await interaction.response.edit_message(embed=embed)
            
        elif select.values[0] == 'category17':
            embed = discord.Embed(title="Categoría 17", description="This is the seventeenth category")
            await interaction.response.edit_message(embed=embed)
       
        else: 
            embed = discord.Embed(title="Error", description="There was an error")
            await interaction.response.edit_message(embed=embed)
        

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h", "commands", "cmd", "helpme", "hlp"])
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="This is the help command")
        await ctx.send(embed=embed, view=HelpView(self.bot))
 
async def setup(bot):
   await bot.add_cog(Help(bot)) 
