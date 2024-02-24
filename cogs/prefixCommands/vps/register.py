from math import e
import os
import discord
import requests
from dotenv import load_dotenv 
from discord.ext import commands

load_dotenv() 
MOMO_API_PTERODACTYL = os.getenv("MOMO_API_PTERODACTYL") 
class Register(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.pterodactyl_api_url = 'https://panel.cinammon.es/api/application/users'
        
        self.pterodactyl_api_key = MOMO_API_PTERODACTYL

    @commands.command(name="register", aliases=['reg','regist', 'cg'])
    async def registration(self, ctx, email:str, username:str, first_name:str, last_name:str, password:str): 
        if ctx.channel.id != 1210710084468875316 and ctx.channel.id != 1210296608596688988:
            return 
        
        user_data = { 
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password 
        }  
        response = self.create_pterodactyl_user(user_data)
        print(f"\nCreated user in Cinammon Hosting:\n-email:{email}\n-username:{username}\n-first name:{first_name}\n-last name:{last_name}\n-password:{password}")
        if 'errors' in response:   
            embed = discord.Embed(title="Registration in Cinammon Hosting", description=f"""<:momostarw:1206266007090364486> {ctx.author.name} **{username}** was registered with {self.bot.user.name}.\n""") 
            embed.set_footer(text="Cinammon Hosting")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.description=f"""<:momostarw:1206266007090364486> {ctx.author.name}, **{username}** was registered with {self.bot.user.name}.\n"""  
            embed.add_field(name="Cinammon Hosting user", value=f"```Information of {username}:\n -email: {email}\n -username: {username}\n -first name: {first_name}\n -last name: {last_name}\n -password: {password}```") 
            await ctx.send(embed=embed, delete_after=120)   
        elif response.get("errors"):
            embed = discord.Embed(title="Registration in Cinammon Hosting", description=f"""<:momostarw:1206266007090364486> {username} was not registered.\n Please check the data and try again.""")
            embed.set_footer(text="Cinammon Hosting")
            await ctx.send(embed=embed, delete_after=120)
        else:
            embed = discord.Embed(title="Registration in Cinammon Hosting", description=f"""<:momostarw:1206266007090364486> {ctx.author.name} **{username}** was successfully registered.\n Thank you for trusting and registering in Cinammon Hosting.""")
            embed.set_footer(text="Cinammon Hosting")
            await ctx.send(embed=embed, delete_after=120)
        await ctx.message.delete()       
    def create_pterodactyl_user(self, user_data):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.pterodactyl_api_key}" 
        } 
        
        response = requests.post(self.pterodactyl_api_url, headers=headers, json=user_data)
        print(response)
        return response.json()

async def setup(bot):
    await bot.add_cog(Register(bot))
