import discord
from discord.ext import commands

class EconomySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Se asume que la conexión a la base de datos ya está establecida y es accesible a través de bot.mysql_connection
        self.mysql_connection = bot.mysql_connection
        self.cursor = self.mysql_connection.cursor()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        user_id = member.id
        guild_id = member.guild.id
        username = member.display_name
        # Verifica si el usuario ya existe y lo registra si no es así
        if not self.user_exists(user_id, guild_id):
            self.register_user(user_id, guild_id, username)
            print(f"Nuevo usuario registrado: {username} (ID: {user_id}) en el servidor {guild_id}.")
        else:
            print(f"El usuario {username} (ID: {user_id}) ya está registrado en el servidor {guild_id}.")

    def register_user(self, user_id, guild_id, username):
        sql = "INSERT INTO users (user_id, guild_id, username, balance) VALUES (%s, %s, %s, %s)"
        val = (user_id, guild_id, username, 0)  # Nuevo usuario con balance inicial de 0
        self.cursor.execute(sql, val)
        self.mysql_connection.commit()

    def user_exists(self, user_id, guild_id):
        sql = "SELECT COUNT(*) FROM users WHERE user_id = %s AND guild_id = %s"
        val = (user_id, guild_id)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        return result[0] > 0 if result else False
    
    def get_balance(self, user_id, guild_id):
        sql = "SELECT balance FROM users WHERE user_id = %s AND guild_id = %s"
        val = (user_id, guild_id)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        return int(result[0]) if result is not None else None
    
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
    
    def cog_unload(self):
        self.cursor.close()
        # No cerramos la conexión aquí, ya que es manejada en otra parte del código

async def setup(bot):
    await bot.add_cog(EconomySystem(bot))
