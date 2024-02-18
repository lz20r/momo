import os
import sys
import asyncio
import random
import discord
import difflib
import requests 
import mysql.connector
import json
from tabulate import tabulate
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.BOT_ID = '1143237780466569306'
        self.used_images = set()

    async def get_image_urls(self):
        image_urls = []
        with open('animes.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line.lower().endswith(('.gif', '.jpeg')):
                    image_urls.append(line)
        return image_urls

    @tasks.loop(minutes=14)
    async def change_avatar(self):
        image_urls = await self.get_image_urls()
        if image_urls:
            available_images = list(set(image_urls) - self.used_images)
            if available_images:
                image_url = random.choice(available_images)
                self.used_images.add(image_url)
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content
                    try:
                        with open("avatar.png", "wb") as f:
                            f.write(image_data)
                    except Exception as e:
                        pass
                    else:
                        with open("avatar.png", "rb") as f:
                            avatar_bytes = f.read()
                        try:
                            await self.bot.user.edit(avatar=avatar_bytes)
                        except discord.HTTPException as e:
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
        
        print(f'Logged in as {self.bot.user.name} ({momoid})')
        await self.change_avatar_loop()

    '''
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
    '''

    async def change_avatar_loop(self):
        while True:
            await self.change_avatar()
            await asyncio.sleep(1200)

async def setup(bot):
    await bot.add_cog(Ready(bot))
