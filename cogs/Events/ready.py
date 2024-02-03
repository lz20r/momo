import os
import sys
import asyncio
import random
import discord
import difflib
import requests 
import mysql.connector
from tabulate import tabulate
from bs4 import BeautifulSoup
from discord.ext import commands 
from discord.ext.commands import CommandNotFound

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.BOT_ID = '1143237780466569306'

    async def get_image_urls(self):
        url = "https://pin.it/47EDzzDhl"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            image_tags = soup.find_all('img')
            image_urls = [tag['src'] for tag in image_tags if 'src' in tag.attrs]
            return image_urls
        else:
            return []

    async def change_avatar(self):
        used_images = set()
        image_urls = await self.get_image_urls()
        if image_urls:
            available_images = list(set(image_urls) - used_images)
            if available_images:
                image_url = random.choice(available_images)
                used_images.add(image_url)
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content
                    await self.bot.user.edit(avatar=image_data)
                else:
                    pass
            else:
                pass
        else:
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready() 

        # Recopila información para la tabla
        momo = self.bot.user.name
        momoid = self.bot.user.id
        servers = len(self.bot.guilds)
        channels = len(set(self.bot.get_all_channels()))
        users = len(self.bot.users)
        members = len(set(self.bot.get_all_members()))
        cogs = len(self.bot.cogs)
        commands = len(self.bot.commands)
        cogs_data = [(x) for x in self.bot.cogs]
        commands_data = [(x.name) for x in self.bot.commands]

        print(f'\n\n------------------------------------------') 
        print(f'Logged in as {self.bot.user.name} ({momoid})') 
        print(f'{momo} status: {self.bot.status.name}')    
        print(f'-------------------------------------------')
        print(f'{momo} is in {servers} servers')
        print(f'{momo} is in {channels} channels')  
        print(f'{momo} has {users} users') 
        print(f'{momo} has {members} members')  
        print(f'-------------------------------------------')
        print(f'Loaded {cogs} cogs')         
        print(f'Loaded {commands} commands') 
        print(f'-------------------------------------------')
        table = tabulate([
            ["Cogs Loaded", "\n".join(cogs_data)],
            ["Commands Loaded", "\n".join(commands_data)],                        
        ], headers=["Cogs & Commands", "Data"], tablefmt="fancy_grid")

        print(table)  
        await self.change_avatar_loop()

    async def change_avatar_loop(self):
        while True:
            await self.change_avatar()
            await asyncio.sleep(1200)

async def setup(bot):
    await bot.add_cog(Ready(bot))