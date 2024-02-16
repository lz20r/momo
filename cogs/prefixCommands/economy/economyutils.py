import os
import json
import discord
from discord.ext import commands

class EconomyUtils(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = "Momo Data"
        os.makedirs(self.data_folder, exist_ok=True)
        self.file_path = os.path.join(self.data_folder, "MomoEconomy.json")  # Ruta al archivo JSON
        self.economy = {}
        self.load_economy_data()
        
    def load_economy_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.economy = json.load(f)
        else:
            with open(self.file_path, 'w') as f:
                json.dump(self.economy, f)
                
    def save_economy_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.economy, f)
            
    def save_economy_data(self, user_data):
        self.economy[user_data["user_id"]] = user_data
        self.save_economy_data()

async def setup(bot):
   await bot.add_cog(EconomyUtils(bot))
