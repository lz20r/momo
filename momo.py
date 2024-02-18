import os   
import asyncio
import pathlib
import discord   
from httpx import get   
import mysql.connector
from dotenv import load_dotenv 
from discord.ext import commands

def get_prefix(): 
    return "m."    

# Intents 

intents = discord.Intents.all()    
bot = commands.Bot(command_prefix=get_prefix(), intents=intents, help_command=None, status=discord.Status.idle)  
      
async def load_extensions():  
    # Load Cogs
    for p in pathlib.Path("cogs").glob("**/*.py"):
        cog_name = p.as_posix()[:-3].replace("/", ".") 
        try: 
            await bot.load_extension(cog_name)
            # print(f"Loaded {cog_name}")  
        except Exception as e:
            print(f"Failed to load {cog_name}: {e}")  

initial_extensions = [
    'cogs.prefixCommands.economy'
] 
# Load Tokens 
load_dotenv() 
token = os.getenv('MOMO_TOKEN') 

initial_extensions = [
    'cogs.prefixCommands.economy'
]
# Load Tokens 
load_dotenv() 
token = os.getenv('MOMO_TOKEN') 
host=os.getenv('momohost')
port=os.getenv('momoport')
user=os.getenv('momouser')
password=os.getenv('momopass')
database=os.getenv('momoname')
# Load Mysql Connection  
async def connection():
    bot.mysql_connection = mysql.connector.connect(
        host,
        port,
        user,
        password,
        database
    )
    bot.cursor = bot.mysql_connection.cursor()
    await bot.mysql_connection.autocommit(True)
    print("Connected to MySQL")

async def main():
    async with bot: 
        await load_extensions() 
        await bot.start(token)

asyncio.run(main()) 
