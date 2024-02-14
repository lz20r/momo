import discord
from discord.ext import commands
from discord.ui import Select, View, Button, button
import random

def pastel_color():
    r = random.randint(180, 255)
    g = random.randint(180, 255)
    b = random.randint(180, 255)
    return discord.Color.from_rgb(r, g, b)


class InviteView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="invite bot", url="https://discord.com/api/oauth2/authorize?client_id=1143237780466569306&permissions=8&scope=bot"))
        self.add_item(Button(label="support", url="https://discord.gg/ezfkXgekw7"))


class InviteBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="invite", aliases=['inv', 'botinvite'])
    async def invite(self, ctx):
        color = pastel_color()

        view = InviteView()
        embed = discord.Embed(color=color, title=f"<:cinnasweat:1205894734539915325> invite {self.bot.user.name} link.", description=f'<:momostarw:1206266007090364486> Our bot is a multifunctional one with the quality of entertainment on [your server](https://discord.com/api/oauth2/authorize?client_id=1143237780466569306&permissions=8&scope=bot), join me so you can enjoy my qualities. We have attentive [support](https://discord.gg/ezfkXgekw7) for any problem.')
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(InviteBot(bot)) 