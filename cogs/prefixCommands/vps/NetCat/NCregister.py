import os
import discord
import requests
from dotenv import load_dotenv 
from discord.ext import commands

load_dotenv() 
NETCAT_API_PTERODACTYL = os.getenv("NETCAT_API_PTERODACTYL")    
class NCRegister(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot  
        self.pterodactyl_api_url = 'https://panel.netcathost.es/api/application/users'
        self.pterodactyl_api_key = NETCAT_API_PTERODACTYL 
        
    @commands.command(name="nctregister", aliases=['ncreg','ncregist', 'nccg'])
    async def registration(self, ctx, email:str, username:str, first_name:str, last_name:str, password:str): 
        momoprefix = await self.bot.get_prefix(ctx.message)
        if ctx.channel.id != 1188102638106062949:
            return 
        
        user_data = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password
        }
        response = self.create_pterodactyl_user(user_data)
        
        if 'errors' in response:   
            embed = discord.Embed(title="Registration in **NetCat Hosting**", description=f"""<:momowarn:1206682132311842878> {username} was not registered.\n
                                  usage: ```Momo Usage: {momoprefix}registration <email> <username> <first name> <last name> <password>```\n""")
            await ctx.send(embed=embed, delete_after=120)
        else:
            embed = discord.Embed(title="Registration in **NetCat Hosting**", description=f"<:momomoon:1206265862684672101> **{username}** was successfully registered.\n Thank you for trusting and registering in NetCat Hosting.") 
            embed.set_footer(text="NetCat Hosting")
            await ctx.send(embed=embed, delete_after=120)

    def create_pterodactyl_user(self, user_data):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.pterodactyl_api_key}" 
        } 
        response = requests.post(self.pterodactyl_api_url, headers=headers, json=user_data)
  
        return response.json()   
    
async def setup(bot):
    await bot.add_cog(NCRegister(bot)) 