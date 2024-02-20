import discord  
from discord.ext import commands 
from cogs.Events.economySystem import EconomySystem 

class balanceView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Deposit", style=discord.ButtonStyle.gray, custom_id="deposit", emoji="💰")
    async def on_deposit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild.id) 
        economy_system = EconomySystem(self.bot)
        user_balance = economy_system.get_balance(user_id, guild_id) 
        max_balance = 1000  
         
        if button.custom_id == "deposit":
            if user_balance > max_balance:
                embed = discord.Embed(description="ups, you already have the maximum balance you can have.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            if user_balance == 0:
                embed = discord.Embed(title="Balance", description=f"{interaction.user}, you have deposited {user_balance} <:momocoins:1209537484153819189>")
                embed.add_field(name="Coins", value=f"{user_balance}", inline=False)
                embed.add_field(
                    name="Momo Bank", 
                    value=f"{user_balance}/{max_balance}",
                    inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title="Balance", description=f"{interaction.user}, you have deposited {user_balance} <:momocoins:1209537484153819189>")
                embed.add_field(name="Coins", value=f"{user_balance}", inline=False)
                embed.add_field(name="Banco", value=f"{user_balance}/{max_balance}", inline=False)
                await interaction.response.send_message(embed=embed)
       
                
    @discord.ui.button(label="Withdraw", style=discord.ButtonStyle.gray, custom_id="withdraw", emoji="💸")
    async def on_withdraw_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild.id) 
        economy_system = EconomySystem(self.bot)
        user_balance = economy_system.get_balance(user_id, guild_id) 
        
        if user_balance is not None:
            embed = discord.Embed( description=" you have withdrawn " + str(user_balance) + " coins.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else: 
            embed = discord.Embed(title="Information of Withdraw", description="You don't have a balance. Momo will give you some coins if you work.")
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
        self.max_balance =  user_balance
        View = balanceView(self.bot)

        if user_balance is not None:
            embed = discord.Embed() 
            embed.add_field(name="Coins", value=f"{user_balance}", inline=True) 
            embed.add_field(name="Banco", value=f"{user_balance}/{self.max_balance}", inline=True)
            embed.set_author(name=user_name, icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed, view=View)
        elif user_id == "None":
            embed = discord.Embed(title="Information of Balance", description="You don't have a balance. Momo will give you some coins if you work.")
            await ctx.send(embed=embed, view=View)
        elif user_balance > self.max_balance:
            embed = discord.Embed(title=f"Balance of {user_tag}",) 
            embed.set_author(name=user_name, icon_url=ctx.author.display_avatar.url)
            embed.add_field(name="Coins", value=f"{user_balance}", inline=True) 
            embed.add_field(name="Banco", value=f"{user_balance}/{self.max_balance}", inline=True)
            await ctx.send(embed=embed, view=View)
        else:
            embed = discord.Embed(title=f"Balance of {user_tag}",) 
            embed.add_field(name="Coins", value=f"{user_balance}", inline=True)  
            await ctx.send(embed=embed, view=View)
 
async def setup(bot):   
    await bot.add_cog(Balance(bot))
