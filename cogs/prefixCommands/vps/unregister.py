import os 
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
        self.pterodactyl_api_key = 'ptla_WQ0gULSSM29XOQ1PT3zvvdxEGSf9tcNM34Vj5vPEKJu'
        
    @commands.command(name="unregister", aliases=['kill','delete', 'ucg'])
    async def unregistration(self, ctx, email:str,): 
        if ctx.channel.id != 1208843557729869935:
            return
            
        user_data = { 
            "email": email,
        }
        print(user_data)
        response = self.delete_pterodactyl_user(user_data) 
        print(response)
        if 'errors' in response:  
            embed = discord.Embed(title="Unregistration in Cinammon Hosting", description=f"""<:momostarw:1206266007090364486> {ctx.author.name} **{username}** was unregistered with {self.bot.user.name}.\n""") 
            embed.set_footer(text="Cinammon Hosting")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.description=f"""<:momostarw:1206266007090364486> {ctx.author.name}, **{username}** was unregistered with {self.bot.user.name}.\n"""  
            embed.add_field(name="Cinammon Hosting user", value=f"```Information of {username}: \n -url: {self.pterodactyl_api_url}\n -email: {email}\n -username: {username}\n -first name: {first_name}\n -last name: {last_name}\n -password: {password}```") 
            await ctx.send(embed=embed, delete_after=120)         
        else:
            embed = discord.Embed(title="Unregistration in Cinammon Hosting", description=f"""<:momostarw:1206266007090364486> {ctx.author.name} **{username}** was successfully unregistered.\n We are sorry to see you go. Thank you for behaving in Cinammon Hosting.""")
            embed.set_footer(text="Cinammon Hosting")
            await ctx.send(embed=embed, delete_after=120)
             
    def delete_pterodactyl_user(self, user_id):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.pterodactyl_api_key}"
        }
        
        # Construye la URL para eliminar el usuario, reemplazando {user_id} con el ID real del usuario
        delete_url = f"https://panel.cinammon.es/api/application/users/{user_id}"

        # Realiza una solicitud DELETE al endpoint construido
        response = requests.delete(delete_url, headers=headers)

        # Devuelve la respuesta JSON de la API
        return response.json() 

async def setup(bot):
    await bot.add_cog(Unregister(bot)) 
