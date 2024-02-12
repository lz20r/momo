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
            ),
            discord.SelectOption(
                label='anime', 
                value='1', 
                description='anime Page'
            )            
        ],
    ) 
    async def select_callback(self, select, interaction: discord.Interaction):
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
            
        if selected_value == "1":
            thumbnail = self.bot.user.avatar_url            
            embed = discord.Embed(
                title="**{} anime page <3**".format(self.bot.user.name),  
                description="Descripción de la categoría 1")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text={}.format(self.bot.user.id), icon_url=self.bot.user.avatar_url) 
            await interaction.response.edit_message(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        
    @commands.command(name="help")
    async def help(self, ctx):
        view = HelpView()
        prefix = await self.bot.get_prefix(ctx.message)
        bot = self.bot
        
        embed = discord.Embed(
            title="**{} help page <3**".format(self.bot.user.name),
            description=f"""**Comandos de {bot.user.name}**
        
        » **Menú de ayuda**\n\n Tenemos `7` categories, `38` `/` and `10` `{prefix}` comandos a explorar. Hay `0` Comandos Secretos.
          
        Lista de comandos: `help <category>`
        Comandos detallados: `help <command>`
        » **Categorías**"
        `{prefix} help action`  ∷ Action
        `{prefix} help anime`  ∷ Anime
        `{prefix} help club`  ∷ Club
        `{prefix} help config`  ∷ Setting
        `{prefix} help currency`  ∷ Economy
        `{prefix} help fun`  ∷ Fun
        `{prefix} help info`  ∷ Information
        `{prefix} help manager`  ∷ Administration
        `{prefix} help marriage`  ∷ Marriages
        `{prefix} help misc`  ∷ Miscellaneous
        `{prefix} help mod`  ∷ Moderation
        `{prefix} help music`  ∷ Music
        `{prefix} help nsfw`  ∷ NSFW
        `{prefix} help reaction`  ∷ Reaction
        `{prefix} help utils`  ∷ Utilities
        `{prefix} help genshin`  ∷ Genshin Impact
        `{prefix} help verify`  ∷ Verification""")   
        await ctx.send(embed=embed, view=view) 

async def setup(bot): 
    await bot.add_cog(Help(bot)) 