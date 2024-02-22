import os   
import asyncio
import pathlib
import discord    
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
            continue
# Load Tokens 
load_dotenv() 
token = os.getenv('MOMO_TOKEN') 

# Load Mysql Connection Details 
host=os.getenv('momohost')
port=os.getenv('momoport')
user=os.getenv('momouser') 
password= os.getenv('momoPass')
database=os.getenv('momoname')
# Load Mysql Connection  
def initialize_mysql_connection():
    config = {
        'user': user,
        'password': password,
        'host': host, 
        'port': port,
        'database': database  
    }   
    return mysql.connector.connect(**config) 
# Assign the MySQL connection to the bot
bot.mysql_connection = initialize_mysql_connection()

# Load your cog (make sure to handle this properly in your bot setup)
async def load_cogs():
    await bot.load_extension('cogs.Events.economySystem') 
    await bot.load_extension('cogs.Events.ticketSystem') 
async def main():
    async with bot: 
        await load_extensions() 
        await bot.start(token)

asyncio.run(main()) 
 