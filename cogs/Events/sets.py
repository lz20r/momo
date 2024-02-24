import re
import discord
import random
import mysql.connector
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor

def randomcolor ():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return (r << 16) + (g << 8) + b

class SetsSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1210624471975854120  # Asegúrate de que este es el ID correcto
        self.mysql_connection = bot.mysql_connection
        self.executor = ThreadPoolExecutor(max_workers=1)   
        
    async def init_mysql(self):
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print(f"No se encontró el canal con ID {self.channel_id}")
            return

        tables = {
            "welcome_guilds": '''
                CREATE TABLE IF NOT EXISTS welcome_guilds (
                    guild_id BIGINT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    channel_id BIGINT,
                    channel_name VARCHAR(255) NOT NULL,
                    message TEXT
                );
            ''',
            "leave_guilds": '''
                CREATE TABLE IF NOT EXISTS leave_guilds (
                    guild_id BIGINT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    channel_id BIGINT,
                    channel_name VARCHAR(255) NOT NULL,
                    message TEXT
                );
            ''',
            "rejoin_guilds": '''
                CREATE TABLE IF NOT EXISTS rejoin_guilds (
                    guild_id BIGINT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    channel_id BIGINT,
                    channel_name VARCHAR(255) NOT NULL,
                    message TEXT
                );
            '''
        }

        await self.create_tables(tables, channel)

    async def create_tables(self, tables, channel):
        loop = self.bot.loop
        for table_name, create_statement in tables.items():
            was_created = await loop.run_in_executor(self.executor, self.create_table, table_name, create_statement)
            if was_created:  
                embed = discord.Embed(
                    title="Created Table",
                    description=f"La tabla `{table_name}` ha sido creada en la base de datos.",
                    color= randomcolor()
                )
                return
                await channel.send(embed=embed)
            else: 
                embed = discord.Embed(
                    title="Existing Tables",
                    description=f"La tabla `{table_name}` ya existe en la base de datos.",
                    color=randomcolor()
                )
                return
                await channel.send(embed=embed)

    def create_table(self, table_name, create_statement):
        cursor = self.mysql_connection.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        if not result:
            cursor.execute(create_statement)
            self.mysql_connection.commit()
            cursor.close()
            return True
        cursor.close()
        return False
      
    def cog_unload(self):
        self.executor.shutdown(wait=False) 
    
    def set_welcome_channel(self, guild_id, channel_id):
        # Insertar o actualizar el canal de bienvenida para un servidor
        conn = mysql.connector.connect(**self.mysql_config)
        cursor = conn.cursor()
        cursor.execute('REPLACE INTO welcome_channels (guild_id, channel_id) VALUES (%s, %s)', (guild_id, channel_id))
        conn.commit()
        conn.close()

    def get_welcome_channel(self, guild_id):
        # Obtener el canal de bienvenida para un servidor
        conn = mysql.connector.connect(**self.mysql_config)
        cursor = conn.cursor()
        cursor.execute('SELECT channel_id FROM welcome_channels WHERE guild_id = %s', (guild_id,))
        channel_id = cursor.fetchone()
        conn.close()
        return channel_id[0] if channel_id else None

    def del_welcome_channel(self, guild_id):
        # Eliminar el canal de bienvenida para un servidor
        conn = mysql.connector.connect(**self.mysql_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM welcome_channels WHERE guild_id = %s', (guild_id,))
        conn.commit()
        conn.close()
        
    def set_leave_channel(self, guild_id, channel_id):
        # Insertar o actualizar el canal de despedida para un servidor
        conn = mysql.connector.connect(**self.mysql_config)
        cursor = conn.cursor()
        cursor.execute('REPLACE INTO leave_channels (guild_id, channel_id) VALUES (%s, %s)', (guild_id, channel_id))
        conn.commit()
        conn.close()
    
    def get_leave_channel(self, guild_id):
        # Obtener el canal de despedida para un servidor
        conn = mysql.connector.connect(**self.mysql_config)
        cursor = conn.cursor()
        cursor.execute('SELECT channel_id FROM leave_channels WHERE guild_id = %s', (guild_id,))
        channel_id = cursor.fetchone()
        conn.close()
        return channel_id[0] if channel_id else None
    
    def del_leave_channel(self, guild_id):
        # Eliminar el canal de despedida para un servidor
        conn = mysql.connector.connect(**self.mysql_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM leave_channels WHERE guild_id = %s', (guild_id,))
        conn.commit()
        conn.close()
        
    def set_rejoin_channel(self, guild_id, channel_id):
        # Insertar o actualizar el canal de bienvenida para un servidor
        conn = mysql.connector.connect(**self.mysql_config)
        cursor = conn.cursor()
        cursor.execute('REPLACE INTO rejoin_channels (guild_id, channel_id) VALUES (%s, %s)', (guild_id, channel_id))
        conn.commit()
        conn.close()
        
    def get_rejoin_channel(self, guild_id):
        # Obtener el canal de bienvenida para un servidor
        conn = mysql.connector.connect(**self.mysql_config)
        cursor = conn.cursor()
        cursor.execute('SELECT channel_id FROM rejoin_channels WHERE guild_id = %s', (guild_id,))
        channel_id = cursor.fetchone()
        conn.close()
        return channel_id[0] if channel_id else None
    
    def del_rejoin_channel(self, guild_id):
        # Eliminar el canal de bienvenida para un servidor
        conn = mysql.connector.connect(**self.mysql_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rejoin_channels WHERE guild_id = %s', (guild_id,))
        conn.commit()
        conn.close()
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.init_mysql()

    def random_color(self):
        return discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
async def setup(bot):
    await bot.add_cog(SetsSystem(bot)) 
