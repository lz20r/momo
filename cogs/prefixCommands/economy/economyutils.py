import os   
import json 
import pathlib
from discord.ext import commands 


class EconomyUtils(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = "Momo Data/Momo Economia"
        os.makedirs(self.data_folder, exist_ok=True)

    def load_economy_data(self, server_id, user_id):
        # Actualizar la ruta del archivo para incluir el ID del servidor en la estructura de la carpeta
        server_folder = os.path.join(self.data_folder, str(server_id))
        os.makedirs(server_folder, exist_ok=True)  

        file_path = os.path.join(server_folder, f'{user_id}.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            # Retornar un diccionario predeterminado con información básica
            return {
                "server_id": server_id,
                "user_id": user_id,
                "username": "Unknown",   
                "balance": 100
            }

    def save_economy_data(self, server_id, user_id, username, balance):
        server_folder = os.path.join(self.data_folder, str(server_id))
        os.makedirs(server_folder, exist_ok=True)

        file_path = os.path.join(server_folder, f'{user_id}.json')
        user_data = {
            "server_id": server_id,
            "user_id": user_id,
            "username": username,
            "balance": balance
        }
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)
            
        return user_data

    def get_top_balances(self, server_id, limit=10):
        server_folder = os.path.join(self.data_folder, str(server_id))
        os.makedirs(server_folder, exist_ok=True)

        top_balances = []
        for file_name in os.listdir(server_folder):
            if file_name.endswith('.json'):
                file_path = os.path.join(server_folder, file_name)
                with open(file_path, 'r') as file:
                    user_data = json.load(file)
                    balance = user_data['balance']
                    top_balances.append((file_name, balance))

        top_balances.sort(key=lambda x: x[1], reverse=True)
        return top_balances[:limit]
    
    def get_top_users(self, server_id, limit=10):
        server_folder = os.path.join(self.data_folder, str(server_id))
        os.makedirs(server_folder, exist_ok=True)

        top_users = []
        for file_name in os.listdir(server_folder):
            if file_name.endswith('.json'):
                file_path = os.path.join(server_folder, file_name)
                with open(file_path, 'r') as file:
                    user_data = json.load(file)
                    balance = user_data['balance']
                    top_users.append((file_name, balance))

        top_users.sort(key=lambda x: x[1], reverse=True)
        return top_users[:limit]
    
    def delete_user_data(self, server_id, user_id):
        server_folder = os.path.join(self.data_folder, str(server_id))
        os.makedirs(server_folder, exist_ok=True)

        file_path = os.path.join(server_folder, f'{user_id}.json')
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return True
    
    def delete_server_data(self, server_id):
        server_folder = os.path.join(self.data_folder, str(server_id))
        if os.path.exists(server_folder):
            os.rmdir(server_folder)
            
        return True
    
    def delete_all_data(self):
        if os.path.exists(self.data_folder):
            os.rmdir(self.data_folder)
            
        return True
    

async def setup(bot):
    await bot.add_cog(EconomyUtils(bot))
