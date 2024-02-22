import os
from re import M 
import requests
import discord 
from dotenv import load_dotenv 
from discord.ext import commands 

load_dotenv()  
MOMO_API_PTERODACTYL = os.getenv("MOMO_API_PTERODACTYL")     
class Unregister(commands.Cog):  
    def __init__(self, bot): 
        self.bot = bot
        self.pterodactyl_api_url = 'https://panel.cinammon.es/api/application/users/'
        self.pterodactyl_api_key = MOMO_API_PTERODACTYL
        
    @commands.command(name="unregister", aliases=['unreg','delete', 'ucg']) 
    async def unregistration(self, ctx, id:int, username:str): 
        if ctx.channel.id != 1208880661939748904:
            return
        response = self.delete_pterodactyl_user(id, username)
        if 'errors' in response:
            embed = discord.Embed(title="Unregistration in Cinammon Hosting", description=f"**{username}** was not unregistered.\n Please check the data and try again.")
            embed.set_footer(text="Cinammon Hosting")
            await ctx.send(embed=embed, delete_after=120)
        else:
            embed = discord.Embed(title="Unregistration in Cinammon Hosting", description=f"**{username}** was successfully unregistered.")
            embed.set_footer(text="Cinammon Hosting")
            await ctx.send(embed=embed, delete_after=120)
        await ctx.message.delete()
    def delete_pterodactyl_user(self, id, username):
        headers = {
            'Authorization': self.pterodactyl_api_key
            
        }
        response = requests.delete(self.pterodactyl_api_url + str(id), headers=headers)
        return response.json()
    

async def setup(bot):
    await bot.add_cog(Unregister(bot)) 
