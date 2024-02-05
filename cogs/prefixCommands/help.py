import discord
from discord.ext import commands
from discord.ui import View, Select, Button


class MySelect(View, commands.Cog):

    @discord.ui.select(
        placeholder='Click for more of kira',
        options=[
            discord.SelectOption(label='home', value='0', description='kira Home Page'),
            discord.SelectOption(label='action', value='1', description='kira Action Commands'),
            discord.SelectOption(label='anime', value='2', description='kira Anime Commands'),
            discord.SelectOption(label='club', value='3', description='kira Club Commands'),
            discord.SelectOption(label='config', value='4', description='kira Setting Commands'),
            discord.SelectOption(label='currency', value='5', description='kira Economy Commands'),
            discord.SelectOption(label='fun', value='6', description='kira Fun Commands'),
            discord.SelectOption(label='info', value='7', description='kira Information Commands'),
            discord.SelectOption(label='manager', value='8', description='kira Administration Commands'),
            discord.SelectOption(label='marriage', value='9', description='kira Marriage Commands'),
            discord.SelectOption(label='misc', value='10', description='kira Miscellaneous Commands'),
            discord.SelectOption(label='mod', value='11', description='kira Moderation Commands'),
            discord.SelectOption(label='music', value='12', description='kira Music Commands'),
            discord.SelectOption(label='nsfw', value='13', description='kira NSFW Commands'),
            discord.SelectOption(label='reaction', value='14', description='kira Reaction Commands'),
            discord.SelectOption(label='utils', value='15', description='kira Utility Commands'),
            discord.SelectOption(label='genshin', value='16', description='kira Genshin Impact Commands'),
            discord.SelectOption(label='verify', value='17', description='kira Verification Commands'),
        ]
    )
    @commands.command(name="ayuda", aliases=["help", "h", "a"])    
    async def ayuda(ctx, self):
        bot = ctx.bot
        prefix = self.bot.get_prefix(ctx.message)   
        view = MySelect()
        thumbnail_url = bot.user.avatar.url
        embed = discord.Embed(
            title="**{} home page <3**".format(bot.user.name), 
            description=
            f"""**Comandos de {bot.user.name}**
            
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
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text=bot.user.name, icon_url=thumbnail_url)
        await ctx.send(embed=embed, view=view) 
