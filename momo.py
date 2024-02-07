import os  
import json
import asyncio
import pathlib
import discord   
from dotenv import load_dotenv 
from discord.ext import commands   


prefix_file = "MomoPrefixes.json"
setprefix_file = "SetMomoPrefix.json"

def save_prefixes(): 
    with open(prefix_file, "w") as file:
        json.dump(custom_prefixes, file)

def load_prefixes():
    try:
        with open(prefix_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_server_prefixes(server_prefixes):
    with open(setprefix_file, "w") as file:
        json.dump(server_prefixes, file)

def load_server_prefixes():
    try:
        with open(setprefix_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def get_prefix(client, message):
    user_id = str(message.author.id)
    server_id = str(message.guild.id)
    default_user_prefix = ["m."]

    if user_id in custom_prefixes:
        return custom_prefixes[user_id]

    elif server_id in server_prefixes:
        return server_prefixes[server_id]

    return default_user_prefix

def set_custom_prefix(user_id, new_prefix):
    custom_prefixes[user_id] = new_prefix
    save_prefixes()

def set_server_prefix(server_id, new_prefix):
    server_prefixes[server_id] = new_prefix
    save_server_prefixes(server_prefixes)

# Intents 
intents = discord.Intents.all()    
client = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None, status=discord.Status.dnd)  

async def load_extensions(): 
    # Load Cogs
    for p in pathlib.Path("cogs").glob("**/*.py"):
        cog_name = p.as_posix()[:-3].replace("/", ".")
        try: 
            await client.load_extension(cog_name)
            #print(f"Loaded {cog_name}")
        except Exception as e:
            print(f"Failed to load {cog_name}: {e}") 

# Load Tokens 
load_dotenv() 
token = os.getenv('MOMO_TOKEN') 

async def main():
    async with client: 
        await load_extensions()
        await client.start(token)

@client.event
async def on_message(message):
    # Cargar nuevamente el prefijo cada vez que se reciba un mensaje
    global custom_prefixes, server_prefixes
    custom_prefixes = load_prefixes()
    server_prefixes = load_server_prefixes()
    await client.process_commands(message)

asyncio.run(main())