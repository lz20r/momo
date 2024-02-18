import os 
import mysql.connector 
from dotenv import load_dotenv 

load_dotenv() 
MOMO_HOST = os.getenv('MOMO_HOST')
MOMO_PORT = os.getenv('MOMO_PORT')
MOMO_USER = os.getenv('MOMO_USER')
MOMO_PASS = os.getenv('MOMO_PASS')
MOMO_NAME = os.getenv('MOMO_NAME')

class EconomySystem:
    def __init__(self, bot):
        self.bot = bot
        self.mysql_connection = mysql.connector.connect(
            host=MOMO_HOST,
            port=MOMO_PORT,
            user=MOMO_USER,
            password=MOMO_PASS,
            database=MOMO_NAME
        )
        self.cursor = self.mysql_connection.cursor()
 
    def register_user(self, user_id, guild_id, username):
            if not self.user_exists(user_id, guild_id):
                sql = "INSERT INTO users (user_id, guild_id, username, balance) VALUES (%s, %s, %s, %s)"
                val = (user_id, guild_id, username, 0)  # Nuevo usuario con balance inicial de 0
                self.cursor.execute(sql, val)
                self.mysql_connection.commit()
                self.mysql_connection.commit()           
            else:
                print("El usuario ya está registrado.")
                return

    def user_exists(self, user_id, guild_id):
        sql = "SELECT COUNT(*) FROM users WHERE guild_id = %s AND user_id = %s"
        val = (user_id, guild_id)
        try:
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()
            return result[0] > 0 if result else False
        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta SQL:", err)
            return False

    def get_balance(self, user_id, guild_id): 
        sql = "SELECT balance FROM users WHERE user_id = %s AND guild_id = %s"
        val = (user_id, guild_id)
        try:
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()
            return int(result[0]) if result is not None else None
        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta SQL:", err)
            return None 
  
    def add_coins(self, user_id, guild_id, amount):
        
        current_balance = self.get_balance(user_id, guild_id)
        if current_balance is not None:
            new_balance = current_balance + amount
            sql = "UPDATE users SET balance = %s WHERE user_id = %s AND guild_id = %s"
            val = (new_balance, user_id, guild_id)
            self.cursor.execute(sql, val)
            self.mysql_connection.commit()
        else:
            self.register_user(user_id, guild_id, 0)  # Si el usuario no existe, regístralo primero
            self.add_coins(user_id, guild_id, amount)  # Llamar de nuevo a esta función


    def remove_coins(self, user_id, guild_id, amount):
        current_balance = self.get_balance(user_id, guild_id)
        if current_balance is not None:
            new_balance = max(current_balance - amount, 0)  # Ensure balance doesn't go negative
            sql = "UPDATE users SET balance = %s WHERE user_id = %s AND guild_id = %s"
            val = (new_balance, user_id, guild_id)
            self.cursor.execute(sql, val)
            self.mysql_connection.commit()
        else:
            print("User not found.")

    def close(self):
        self.cursor.close()
        self.mysql_connection.close()
        print("MySQL connection closed.")

async def setup(bot):
    await bot.add_cog(EconomySystem(bot))
