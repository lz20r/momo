import os  
import json
import asyncio
import pathlib
import discord   
from dotenv import load_dotenv 
from discord.ext import commands
from httpx import get   


def get_prefix(): 
    return "m." 

# Intents 
intents = discord.Intents.all()    
client = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None, status=discord.Status.dnd)  

@commands.Cog.listener()
async def on_message(message): 
    if message.content.startswith(client.user.mention):
        user_prefixes = get_prefix(client, message)
        user_id = str(message.author.id)   
        user_prefix = ''.join(user_prefixes) if user_prefixes else None
        if user_id not in get_prefix:
            embed_hello = discord.Embed(title="", description=f"<:8_wngs:1200775867673104526> my prefix here is: `{user_prefix}`")
            await message.reply(embed=embed_hello)
        else:
            embed = discord.Embed(title="", description=f"<:line:1194496410167549963> self prefix is: `{user_prefix}`")
            await message.reply(embed=embed)

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

asyncio.run(main())
