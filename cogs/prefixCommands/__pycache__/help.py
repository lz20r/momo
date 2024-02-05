import discord
from discord.ext import commands

class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Ayuda del Bot", color=discord.Color.blue())
        embed.set_thumbnail(url="URL_DE_TU_LOGO")  # Opcional: Añade el logo de tu bot
        for cog, commands in mapping.items():
            filtered_commands = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered_commands]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Sin Categoría")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
        
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f"{cog.qualified_name} - Comandos", color=discord.Color.green())
        filtered_commands = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered_commands:
            embed.add_field(name=self.get_command_signature(command), value=command.short_doc or "Sin descripción", inline=False)
        
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=self.get_command_signature(group), description=group.short_doc, color=discord.Color.orange())
        filtered_commands = await self.filter_commands(group.commands, sort=True)
        for command in filtered_commands:
            embed.add_field(name=self.get_command_signature(command), value=command.short_doc or "Sin descripción", inline=False)
        
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), description=command.help, color=discord.Color.red())
        channel = self.get_destination()
        await channel.send(embed=embed)

bot = commands.Bot(command_prefix="!", help_command=CustomHelpCommand())

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(help="Muestra este mensaje de ayuda.")
async def ayuda(ctx):
    """Este comando muestra el mensaje de ayuda."""
    await ctx.send_help()

async def setup(bot)
          await bot.add_cog(CustomHelpCommand(bot))