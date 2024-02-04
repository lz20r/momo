import os 
import requests
from dotenv import load_dotenv 
from discord.ext import commands
load_dotenv() 
MOMO_API_PTERODACTYL = os.getenv("MOMO_API_PTERODACTYL")    
class Registro(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.pterodactyl_api_url = 'https://panel.cinammon.es/api/application/users'
        self.pterodactyl_api_key = MOMO_API_PTERODACTYL

    @commands.command()
    async def registro(self, ctx, email:str, username:str, first_name:str, last_name:str, password:str):
        if ctx.channel.name != '1202405777617191023':
            return
        
        user_data = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "las_name": last_name,
            "password": password
        }

        response = self.create_pterodactyl_user(user_data)
        print(response)

        if response.status_code == 201:  
            await ctx.send(f"Usuario {username} registrado con éxito en el sistema.")
        else:
            await ctx.send("Hubo un error al registrar el usuario. Por favor, intenta nuevamente.")

    def create_pterodactyl_user(self, user_data):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.pterodactyl_api_key}" 
        } 
        
        response = requests.post(self.pterodactyl_api_url, headers=headers, data=user_data)
        print(response)
        return response.json()

async def setup(bot):
    await bot.add_cog(Registro(bot))
