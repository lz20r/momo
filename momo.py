import os  
import json
import asyncio
import pathlib
import discord   
from httpx import get   
from dotenv import load_dotenv 
from discord.ext import commands

def get_prefix(): 
    return "m."    

# Intents 
intents = discord.Intents.all()    
client = commands.Bot(command_prefix=get_prefix(), intents=intents, help_command=None, status=discord.Status.idle)  
      
async def load_extensions(): 
    # Load Cogs
    for p in pathlib.Path("cogs").glob("**/*.py"):
        cog_name = p.as_posix()[:-3].replace("/", ".") 
        try: 
            await client.load_extension(cog_name)
            # print(f"Loaded {cog_name}")  
        except Exception as e:
            print(f"Failed to load {cog_name}: {e}")  

initial_extensions = [
    'cogs.prefixCommands.economy'
]
# Load Tokens 
load_dotenv() 
token = os.getenv('MOMO_TOKEN') 

async def main():
    async with client: 
        await load_extensions()
        await client.start(token)

asyncio.run(main())
