from math import e
from os import times
import discord  
from discord.ext import commands 
from cogs.Events.economySystem import EconomySystem 

class balanceView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Deposit", style=discord.ButtonStyle.gray, custom_id="deposit")
    async def on_deposit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild.id) 
        economy_system = EconomySystem(self.bot)
        user_balance = economy_system.get_balance(user_id, guild_id)

        if button.custom_id == "deposit":
            if user_balance is not None:
                embed = discord.Embed(title="Deposit", description=f"{interaction.user.mention} your balance is {user_balance}.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Information of Deposit", description="You don't have a balance. Use `{self.bot.command_prefix}deposit <amount>` or  `{self.bot.command_prefix}work` to get some coins.") 
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
    @discord.ui.button(label="Withdraw", style=discord.ButtonStyle.red, custom_id="withdraw")
    async def on_withdraw_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild.id) 
        economy_system = EconomySystem(self.bot)
        user_balance = economy_system.get_balance(user_id, guild_id)

        if button.custom_id == "withdraw":
            if user_balance is not None:
                embed = discord.Embed(title="Withdraw", description=f"{interaction.user.mention} you have withdrawn {user_balance}.")
                embed.set_footer(text="Balance System") 
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Information of Withdraw", description="You don't have a balance. Use `{self.bot.command_prefix}deposit <amount>` or  `{self.bot.command_prefix}work` to get some coins.") 
                await interaction.response.send_message(embed=embed, ephemeral=True) 
                
class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_system = EconomySystem(bot)
        
    @commands.command(name='saldo', aliases=['bal']) 
    async def balance(self, ctx): 
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id) 
        guild_name = str(ctx.guild.name)
        user_name = str(ctx.author.name)
        user_tag = str(ctx.author)
        user_balance = self.economy_system.get_balance(user_id, guild_id)

        View = balanceView(self.bot)

        if user_balance is not None:
            embed = discord.Embed(title=f"Balance of {user_tag}", description=f"{user_name} having {user_balance} coins.")
            embed.set_footer(text=f"{self.bot.user.name}'s Balance System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed, view=View)
        elif user_balance == 0:
            embed = discord.Embed(title=f"Balance of {user_tag}", description=f"{user_name} having {user_balance} coins.")
            embed.set_footer(text=f"{self.bot.user.name}'s Balance System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed, view=View)
        elif user_balance > self.max_balance:
            embed = discord.Embed(title="Error", description=f"{user_name} en {guild_name}, no puedes tener más de {self.max_balance} monedas.")
            embed.set_footer(text=f"{self.bot.user.name}'s Balance System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed, view=View)
        else:
            embed = discord.Embed(title="Error", description=f"{user_name} en {guild_name}, no tienes ninguna moneda.")
            embed.set_footer(text=f"{self.bot.user.name}'s Balance System")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed, view=View)
 
async def setup(bot):  
    await bot.add_cog(Balance(bot))
