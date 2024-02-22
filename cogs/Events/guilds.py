from discord.ext import commands
 

class Guilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Se asume que la conexión a la base de datos ya está establecida y es accesible a través de bot.mysql_connection
        self.mysql_connection = bot.mysql_connection
        self.cursor = self.mysql_connection.cursor()
        self.channelguildid = "1208808029726834769"
    def register_users(self, ctx):
        sql = """
        DROP TABLE IF EXISTS guilds;
        CREATE TABLE guilds(
            id INT(11) NOT NULL PRIMARY KEY auto_increment,
            user_id VARCHAR(255) NOT NULL,
            guild_id VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            guildname VARCHAR(255) NOT NULL,
            members  VARCHAR(255) NOT NULL
        );
        """ 
        self.cursor.execute(sql)
        self.mysql_connection.commit() 
        
    def on_member_join(self, member, ctx):
        sql = "INSERT INTO guilds (user_id, guild_id, username, guildname, members) VALUES (%s, %s, %s, %s, %s)"
        val = (member.id, member.guild.id, member.name, member.guild.name, 1)
        self.cursor.execute(sql, val)
        self.mysql_connection.commit()
        print(f"Registered {member.name} ({member.id}) in {member.guild.name} ({member.guild.id})")
        
    def on_member_remove(self, member):
        sql = "UPDATE guilds SET members = members - 1 WHERE user_id = %s AND guild_id = %s"
        val = (member.id, member.guild.id)
        self.cursor.execute(sql, val)
        
        sql = "SELECT members FROM guilds WHERE user_id = %s AND guild_id = %s"
        val = (member.id, member.guild.id)
        self.cursor.execute(sql, val)
        
        result = self.cursor.fetchone()
        if result[0] == 0:
            sql = "DELETE FROM guilds WHERE user_id = %s AND guild_id = %s"
            val = (member.id, member.guild.id)
            self.cursor.execute(sql, val)
        self.mysql_connection.commit()
        
        print(f"Unregistered {member.name} ({member.id}) from {member.guild.name} ({member.guild.id})")
        
    def on_guild_join(self, guild):
        sql = "INSERT INTO guilds (user_id, guild_id, username, guildname, members) VALUES (%s, %s, %s, %s, %s)"
        val = (guild.owner_id, guild.id, guild.owner.name, guild.name, guild.member_count)
        self.cursor.execute(sql, val)
        self.mysql_connection.commit()
        print(f"Registered {guild.owner.name} ({guild.owner.id}) in {guild.name} ({guild.id})")
        
    def on_guild_remove(self, guild):
        sql = "DELETE FROM guilds WHERE guild_id = %s"
        val = (guild.id,)
        self.cursor.execute(sql, val)
        self.mysql_connection.commit()
        print(f"Unregistered {guild.name} ({guild.id})")
        
    def on_guild_update(self, before, after):
        sql = "UPDATE guilds SET guildname = %s WHERE guild_id = %s"
        val = (after.name, after.id)
        self.cursor.execute(sql, val)
        self.mysql_connection.commit()
        print(f"Updated {before.name} ({before.id}) to {after.name} ({after.id})")
        
    def on_member_update(self, before, after):
        sql = "UPDATE guilds SET username = %s WHERE user_id = %s AND guild_id = %s"
        val = (after.name, after.id, after.guild.id)
        self.cursor.execute(sql, val)
        self.mysql_connection.commit()
        print(f"Updated {before.name} ({before.id}) to {after.name} ({after.id})")
        
    def on_member_ban(self, guild, user):
        sql = "DELETE FROM guilds WHERE user_id = %s AND guild_id = %s"
        val = (user.id, guild.id)
        self.cursor.execute(sql, val)
        self.mysql_connection.commit()
        
    def on_member_unban(self, guild, user):
        sql = "INSERT INTO guilds (user_id, guild_id, username, guildname, members) VALUES (%s, %s, %s, %s, %s)"
        val = (user.id, guild.id, user.name, guild.name, 1)
        self.cursor.execute(sql, val)
        self.mysql_connection.commit()

    def cog_unload(self):
        self.mysql_connection.close()
        self.cursor.close()
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.create_table()
        
        
async def setup(bot):
    await bot.add_cog(Guilds(bot))
