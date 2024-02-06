import os
import mysql.connector
from tabulate import tabulate
from discord.ext import commands

class PrefixConnection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        db_setup_result = self.setup_database()

        s3_momoDB = "s3_momoDB"
        prefix = "prefix"
        historialprefix = "historialprefix"
        prefix_file = "../cogs/Events/database/prefixConnection.py"
 
        table_data = [ 
            [f'{prefix_file}', f"{s3_momoDB} connected!" if db_setup_result is True else f"{s3_momoDB} already exists!"],
            [f'{prefix_file}', f"{prefix} created!" if db_setup_result is True else f"{prefix} already exists!"],
            [f'{prefix_file}', f"{historialprefix} created!" if db_setup_result is True else f"{historialprefix} already exists!"]
        ]

        table = tabulate(table_data, headers=["Dir", "Status"], tablefmt="fancy_grid")

        print(table)

    def setup_database(self):
        try:
            connection = mysql.connector.connect(
                host=os.environ['DB_HOST'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASS'],
                database=os.environ['DB_NAME']
            )

            cursor = connection.cursor()
            connection.commit()
            cursor.close()

            cursor = connection.cursor(buffered=True)
            cursor.execute("USE s3_momoDB")
            cursor.execute("DROP TABLE IF EXISTS prefijos")
            cursor.execute("DROP TABLE IF EXISTS prefix")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS prefix (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    server_id BIGINT NOT NULL,
                    server_name VARCHAR(255) NOT NULL,                
                    user_name VARCHAR(255) NOT NULL,
                    prefix VARCHAR(100) NOT NULL,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
            """)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS historialprefix (
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    user_name VARCHAR(255) NOT NULL,
                    server_id BIGINT NOT NULL, 
                    server_name VARCHAR(255) NOT NULL,
                    old_prefix VARCHAR(10) NOT NULL, 
                    new_prefix VARCHAR(10) NOT NULL, 
                    changed_by BIGINT NOT NULL, 
                    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);
            """)

            connection.commit()
            cursor.close()

            return True
        except Exception as e:
            return str(e)
        
async def setup(bot):
    await bot.add_cog(PrefixConnection(bot)) 
