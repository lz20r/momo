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

    def delete_pterodactyl_user(self, user_id):
            delete_url = f'{self.pterodactyl_api_url}/{user_id}'

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",                
                "Authorization": f"Bearer {self.pterodactyl_api_key}"
            }

            response = requests.delete(delete_url, headers=headers)

            if response.status_code == 204:
                return {"message": "Usuario eliminado con éxito."}
            else:
                return {"error": "Error al eliminar el usuario."}

    @commands.command(name="unregistration", aliases=['unreg','unregist', 'ur'])
    async def unregistration(self, ctx, user_id: int):
        if ctx.channel.id != 1202155438679019580:
            return  
        
        response = self.delete_pterodactyl_user(user_id)
        if 'error' in response:
            await ctx.send("Hubo un error al eliminar el usuario. Por favor, intenta nuevamente.")
        else:
            await ctx.send("Usuario eliminado con éxito de la API de Pterodactyl.")

async def setup(bot):
    await bot.add_cog(Registro(bot))
