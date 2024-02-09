import discord
from discord.ext import commands
from discord.ui import Select, View

class HelpView(View):
    @discord.ui.select(
        placeholder='Click more for momo',
        options=[
            discord.SelectOption(
                label='home', 
                value='0', 
                description='momo Home Page'
            )
        ],
    )
    
    async def select_callback(self, select interaction):
        select.disabled = True
        selected_value = interaction.data["values"][0]

        if selected_value == "0":
            embed = discord.Embed(title="Categoría 1", description="Descripción de la categoría 1")
            await interaction.response.edit_message(embed=embed)
        elif selected_value == "category2":
            embed = discord.Embed(title="Categoría 2", description="Descripción de la categoría 2")
            await interaction.response.edit_message(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        view = HelpView(self.bot)
        message = await ctx.send("Selecciona una categoría:", view=view)
        view.message = message 
async def setup(bot):
    await bot.add_cog(Help(bot))