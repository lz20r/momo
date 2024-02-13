import os 
import requests
from dotenv import load_dotenv 
from discord.ext import commands

load_dotenv() 
MOMO_API_PTERODACTYL = os.getenv("MOMO_API_PTERODACTYL")    
class Registro(commands.Cog, name="registro"): 
    def __init__(self, bot):
        self.bot = bot
        self.pterodactyl_api_url = 'https://panel.cinammon.es/api/application/users'
        self.pterodactyl_api_key = MOMO_API_PTERODACTYL
        
    @commands.command(name="registro", aliases=['reg','regist', 'cg'])
    async def registration(self, ctx, email:str, username:str, first_name:str, last_name:str, password:str):
        # 1202405777617191023
        if ctx.channel.id != 1202155438679019580:
            return
            
        user_data = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password
        }
        
        response = self.create_pterodactyl_user(user_data)
        print(response)

        if 'errors' in response:  
            await ctx.send("Hubo un error al registrar el usuario. Por favor, intenta nuevamente.")
            print(user_data["username"])
            print(response["errors"])
        else:
            await ctx.send(f"Usuario {username} registrado con éxito en el sistema.")

    def create_pterodactyl_user(self, user_data):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.pterodactyl_api_key}" 
        } 
        
        response = requests.post(self.pterodactyl_api_url, headers=headers, json=user_data)
  
        return response.json()  
