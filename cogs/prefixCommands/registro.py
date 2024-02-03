import os
import json
import discord
import requests
from discord.ext import commands

class Registro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pterodactyl_api_url = 'https://panel.cinammon.es/api/application/users'
        self.pterodactyl_api_key = os.getenv('MOMO_API_PTERODACTYL')

    @commands.command(name="registro", aliases=["reg", "register", "registrar"])
    async def registro(self, ctx, email:str, username:str, first_name:str, last_name:str, password:str):
        if ctx.channel.name != '1202405777617191023':
            return
        
        user_data = {
            "email": email,
            "username":  username,
			"first_name": first_name,
            "las_name": last_name,
            "password": password
        }

        response = self.creat_user(user_data) 
        print(response)

        if response.status_code == 201:  
            await ctx.send(f"Usuario {username} registrado con éxito en el sistema.")
        else:
            await ctx.send("Hubo un error al registrar el usuario. Por favor, intenta nuevamente.")

    def create_user(self, user):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.pterodactyl_api_key}"
        }
        response = requests.post(self.pterodactyl_api_url, headers=headers, data=json.dumps(user))
         
        return response.json()
async def setup(bot):
    await bot.add_cog(Registro(bot))

 