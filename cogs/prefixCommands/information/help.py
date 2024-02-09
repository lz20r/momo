import discord
from discord.ext import commands
from discord.ui import Select, View

from main import icon

class HelpView(View):
    @discord.ui.select(
        placeholder='Click more for momo',
        options=[
            discord.SelectOption(
                label='home', 
                value='0', 
                description='momo Home Page'
            ),
            discord.SelectOption(
                label='home', 
                value='1', 
                description='anime Page'
            )            
        ],
    )
    
    async def select_callback(self, select, interaction):
        select.disabled = True
        selected_value = interaction.data["values"][0]

        if selected_value == "0":
            thumbnail = self.bot.user.avatar_url
            embed = discord.Embed(
                title="**{} home page <3**".format(self.bot.user.name),  
                description="Descripción de la categoría 0")
            embed.set_thumbnail(url=thumbnail)
            embed.set_footer(text={}.format(self.bot.user.id), icon_url=self.bot.user.avatar_url) 
            await interaction.response.edit_message(embed=embed)
            
        if selected_value == "0":
            thumbnail = self.bot.user.avatar_url            
            embed = discord.Embed(
                title="**{} home page <3**".format(self.bot.user.name),  
                description="Descripción de la categoría 1")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text={}.format(self.bot.user.id), icon_url=self.bot.user.avatar_url) 
            await interaction.response.edit_message(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        view = HelpView(self.bot)
        message = await ctx.send("Selecciona una categoría:", view=view)
        view.message = message 
async def setup(bot): 
    await bot.add_cog(Help(bot)) 
