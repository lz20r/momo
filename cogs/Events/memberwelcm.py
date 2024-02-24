import discord
import random
from discord.ext import commands

def random_pastel_color():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return (r << 16) + (g << 8) + b

class Welcome(commands.Cog):
    def __init__(self,bot) -> None: 
        self.bot = bot
        self.mysql_connection = bot.mysql_connection
    
    @commands.command(name='setwlcmTitle', alisases= ['swt'], help='Establece el título del mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_title(self, ctx, *, title: str):
        guild_id = ctx.guild.id
        username = ctx.author.name
        cursor = self.mysql_connection.cursor()
        query = '''
            INSERT INTO welcome_guilds (guild_id, username, title) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            title=%s
        '''
        cursor.execute(query, (guild_id, username, title, title))
        self.mysql_connection.commit()
        cursor.close()
        if cursor.rowcount:
            embed = discord.Embed(title='Título de Bienvenida Establecido', description='El título del mensaje de bienvenida ha sido configurado.', color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Error', description='No se ha podido establecer el título del mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
            
    @commands.command(name='delwlcmTitle', alisases= ['dwt'], help='Elimina el título del mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def del_welcome_title(self, ctx):
        guild_id = ctx.guild.id
        cursor = self.mysql_connection.cursor()
        query = 'DELETE FROM welcome_guilds WHERE guild_id = %s'
        cursor.execute(query, (guild_id,))
        self.mysql_connection.commit()
        cursor.close()
        if cursor.rowcount:
            embed = discord.Embed(title='Título de Bienvenida Eliminado', description='El título del mensaje de bienvenida ha sido eliminado.', color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Error', description='No se ha podido eliminar el título del mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
            
    @commands.command(name='showwlcmTitle', alisases= ['swt'], help='Muestra el título del mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def show_welcome_title(self, ctx):
        guild_id = ctx.guild.id
        cursor = self.mysql_connection.cursor()
        query = 'SELECT title FROM welcome_guilds WHERE guild_id = %s'
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            title = result[0]
            embed = discord.Embed(title='Título de Bienvenida', description=title, color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Título de Bienvenida', description='No se ha configurado el título del mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
    
    @commands.command(name='setwlcmimg', alisases= ['swi'], help='Establece la imagen del mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_image(self, ctx, image: str):
        guild_id = ctx.guild.id
        username = ctx.author.name
        cursor = self.mysql_connection.cursor()
        query = '''
            INSERT INTO welcome_guilds (guild_id, username, image) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            image=%s
        '''
        cursor.execute(query, (guild_id, username, image, image))
        self.mysql_connection.commit()
        cursor.close()
        if cursor.rowcount:
            embed = discord.Embed(title='Imagen de Bienvenida Establecida', description='La imagen del mensaje de bienvenida ha sido configurada.', color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Error', description='No se ha podido establecer la imagen del mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
            
    @commands.command(name='delwlcmimg', alisases= ['dwi'], help='Elimina la imagen del mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def del_welcome_image(self, ctx):
        guild_id = ctx.guild.id
        cursor = self.mysql_connection.cursor()
        query = 'DELETE FROM welcome_guilds WHERE guild_id = %s'
        cursor.execute(query, (guild_id,))
        self.mysql_connection.commit()
        cursor.close()
        if cursor.rowcount:
            embed = discord.Embed(title='Imagen de Bienvenida Eliminada', description='La imagen del mensaje de bienvenida ha sido eliminada.', color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Error', description='No se ha podido eliminar la imagen del mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
            
    @commands.command(name='showwlcmimg', alisases= ['swi'], help='Muestra la imagen del mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def show_welcome_image(self, ctx):
        guild_id = ctx.guild.id
        cursor = self.mysql_connection.cursor()
        query = 'SELECT image FROM welcome_guilds WHERE guild_id = %s'
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            image = result[0]
            embed = discord.Embed(title='Imagen de Bienvenida', description=image, color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Imagen de Bienvenida', description='No se ha configurado la imagen del mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
    
    @commands.command(name='setwlcmcolor', alisases= ['swc'], help='Establece el color del mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_color(self, ctx, color: str):
        guild_id = ctx.guild.id
        username = ctx.author.name
        cursor = self.mysql_connection.cursor()
        query = '''
            INSERT INTO welcome_guilds (guild_id, username, color) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            color=%s
        '''
        cursor.execute(query, (guild_id, username, color, color))
        self.mysql_connection.commit()
        cursor.close()
        if cursor.rowcount:
            embed = discord.Embed(title='Color de Bienvenida Establecido', description='El color del mensaje de bienvenida ha sido configurado.', color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Error', description='No se ha podido establecer el color del mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
            
    @commands.command(name='delwlcmcolor', alisases= ['dwc'], help='Elimina el color del mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def del_welcome_color(self, ctx):
        guild_id = ctx.guild.id
        cursor = self.mysql_connection.cursor()
        query = 'DELETE FROM welcome_guilds WHERE guild_id = %s'
        cursor.execute(query, (guild_id,))
        self.mysql_connection.commit()
        cursor.close()
        if cursor.rowcount:
            embed = discord.Embed(title='Color de Bienvenida Eliminado', description='El color del mensaje de bienvenida ha sido eliminado.', color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Error', description='No se ha podido eliminar el color del mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
            
    @commands.command(name='showwlcmcolor', alisases= ['swc'], help='Muestra el color del mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def show_welcome_color(self, ctx):
        guild_id = ctx.guild.id
        cursor = self.mysql_connection.cursor()
        query = 'SELECT color FROM welcome_guilds WHERE guild_id = %s'
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            color = result[0]
            embed = discord.Embed(title='Color de Bienvenida', description=color, color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Color de Bienvenida', description='No se ha configurado el color del mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
            
    
    @commands.command(name='setwelcomemsg', alisases= ['swm'], help='Establece el mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_message(self, ctx, *, message: str):
        guild_id = ctx.guild.id
        username = ctx.author.name
        channel_id = ctx.channel.id
        channel_name = ctx.channel.name

        cursor = self.mysql_connection.cursor()
        query = '''
            INSERT INTO welcome_guilds (guild_id, username, channel_id, channel_name, message) 
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            message=%s
        '''
        cursor.execute(query, (guild_id, username, channel_id, channel_name, message, message))
        self.mysql_connection.commit()
        cursor.close() 
        if cursor.rowcount:
            embed = discord.Embed(title='Mensaje de Bienvenida Establecido', description='El mensaje de bienvenida ha sido configurado.', color=random_pastel_color())
            await ctx.send(embed=embed) 
        else:
            embed = discord.Embed(title='Error', description='No se ha podido establecer el mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
    
    @commands.command(name='showwelcom', alisases= ['sw'], help='Muestra el mensaje y el canal de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def show_welcome(self, ctx):
        guild_id = ctx.guild.id
        cursor = self.mysql_connection.cursor()
        query = 'SELECT channel_id, channel_name, message FROM welcome_guilds WHERE guild_id = %s'
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            channel_id, channel_name, message = result
            embed = discord.Embed(title='Configuración de Bienvenida', color=random_pastel_color())
            embed.add_field(name='Canal de Bienvenida', value=f'{channel_name} ({channel_id})', inline=False)
            embed.add_field(name='Mensaje de Bienvenida', value=message, inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Configuración de Bienvenida', description='No se ha configurado el mensaje y el canal de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)   
            
    @commands.command(name='delwelcomemsg', alisases= ['dwm'], help='Elimina el mensaje de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def del_welcome_message(self, ctx):
        guild_id = ctx.guild.id
        cursor = self.mysql_connection.cursor()
        query = 'DELETE FROM welcome_guilds WHERE guild_id = %s'
        cursor.execute(query, (guild_id,))
        self.mysql_connection.commit()
        cursor.close()
        if cursor.rowcount:
            embed = discord.Embed(title='Mensaje de Bienvenida Eliminado', description='El mensaje de bienvenida ha sido eliminado.', color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Error', description='No se ha podido eliminar el mensaje de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
            
    @commands.command(name='setwelcome', alisases= ['sw'], help='Establece el canal de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        guild_id = ctx.guild.id
        username = ctx.author.name
        channel_id = channel.id
        channel_name = channel.name

        cursor = self.mysql_connection.cursor()
        query = '''
            INSERT INTO welcome_guilds (guild_id, username, channel_id, channel_name) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            channel_id=%s, channel_name=%s
        '''
        cursor.execute(query, (guild_id, username, channel_id, channel_name, channel_id, channel_name))
        self.mysql_connection.commit()
        cursor.close()
        if cursor.rowcount:
            embed = discord.Embed(title='Canal de Bienvenida Establecido', description=f'El canal de bienvenida ha sido configurado en {channel.mention}.', color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Error', description='No se ha podido establecer el canal de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed)
            
    @commands.command(name='delwelcome', alisases= ['dw'], help='Elimina el canal de bienvenida para nuevos miembros.')
    @commands.has_permissions(manage_guild=True)
    async def del_welcome_channel(self, ctx):
        guild_id = ctx.guild.id
        cursor = self.mysql_connection.cursor()
        query = 'DELETE FROM welcome_guilds WHERE guild_id = %s'
        cursor.execute(query, (guild_id,))
        self.mysql_connection.commit()
        cursor.close()
        if cursor.rowcount:
            embed = discord.Embed(title='Canal de Bienvenida Eliminado', description='El canal de bienvenida ha sido eliminado.', color=random_pastel_color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Canal de Bienvenida Eliminado', description='No se ha podido eliminar el canal de bienvenida.', color=random_pastel_color())
            await ctx.send(embed=embed) 
     
async def setup(bot):
    await bot.add_cog(Welcome(bot))
    

    