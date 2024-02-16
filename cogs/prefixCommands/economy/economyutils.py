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


"""
def load_cash_data():
    globalchat_direc = 'launted database'
    cash_file = os.path.join(globalchat_direc, 'cash.json')
    if os.path.exists(cash_file):
        with open(cash_file, "r") as f:
            return json.load(f)
    else:
        return {}

def save_cash_data(data):
    globalchat_direc = 'launted database'
    cash_file = os.path.join(globalchat_direc, 'cash.json')
    with open(cash_file, "w") as f:
        json.dump(data, f, indent=4)

@client.command(name='withdraw', aliases=['wd'])
async def withdraw(ctx, amount: Union[int, str] = None):
    user_id = str(ctx.author.id)
    globalchat_direc = 'launted database'
    bank_file = os.path.join(globalchat_direc, 'bank.json')

    if os.path.exists(bank_file):
        with open(bank_file, "r") as f:
            bank_data = json.load(f)
    else:
        bank_data = {}

    bank_balance = bank_data.get(user_id, 0)

    if amount is None:
        embed = discord.Embed(description=f'<:launted:1203119545213128735> provide the amount to withdraw.')
        await ctx.send(embed=embed)
        return
    
    if isinstance(amount, str) and amount.lower() == 'all':
        amount = bank_balance

    try:
        amount = int(amount)
    except ValueError:
        embed = discord.Embed(description=f'<:launted:1203119545213128735> invalid amount.')
        await ctx.send(embed=embed)
        return

    if amount <= bank_balance:
        bank_data[user_id] -= amount
        with open(bank_file, "w") as f:
            json.dump(bank_data, f, indent=4)

        cash_data = load_cash_data()

        cash_data[user_id] = cash_data.get(user_id, 0) + amount

        save_cash_data(cash_data)
        embed = discord.Embed(description=f'<:launtedbank:1206215039858642984> **Withdrew** <:launtedbag:1206214723847061604> ${amount} cash from bank!')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f"<:launted:1203119545213128735> You don't have enough cash in the bank to withdraw.")
        await ctx.send(embed=embed)

COOLDOWN_ROBO = 60

@client.command()
@commands.cooldown(1, COOLDOWN_ROBO, commands.BucketType.user)
async def rob(ctx):
    globalchat_direc = 'launted database'
    cash_file = os.path.join(globalchat_direc, 'cash.json')
    
    try:
        with open(cash_file, "r") as f:
            cash_data = json.load(f)
        
        if not cash_data:
            embed = discord.Embed(description=f'<:launted:1203119545213128735> no found person to rob in the server.')
            await ctx.send(embed=embed)
            return
        
        all_users = [user_id for user_id in cash_data.keys() if user_id != str(ctx.author.id)]
        
        
        if not all_users:
            embed = discord.Embed(description=f'<:launted:1203119545213128735> no found person to rob in the server.')
            await ctx.send(embed=embed)
            return
        
        user_id = random.choice(all_users)

        if cash_data[user_id] == 0:
            embed = discord.Embed(description=f'<:launted:1203119545213128735> Oh no, you found nothing to steal!')
            return await ctx.send(embed=embed)
        
        if random.random() < 0.7:
            porcentaje = random.randint(1, 15)
            monto_a_robar = int(cash_data[user_id] * (porcentaje / 100))
            cash_data[user_id] -= monto_a_robar
            with open(cash_file, "w") as f:
                json.dump(cash_data, f, indent=4)
            embed = discord.Embed(description=f'<:launtedrobbery:1206216738589376592> You stole <:launtedbag:1206214723847061604> $**{monto_a_robar}** of cash from user <@{user_id}>.')
        else:
            embed = discord.Embed(description=f"<:launtedrobbery:1206216738589376592> oops, you failed in the robbery you were imprisoned for 1 minute")
        
        await ctx.send(embed=embed)

    except Exception as e:
        pass
"""
