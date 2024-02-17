import discord
from discord.ext import commands, menus

class RoleSelect(menus.ListPageSource):
    def __init__(self, roles, per_page=10):
        self.roles = roles
        super().__init__(roles, per_page=per_page)

    async def format_page(self, menu, roles):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title="Roles en el servidor", color=discord.Color.blue())

        for i, role in enumerate(roles, start=offset):
            embed.add_field(name=f"Rol {i+1}", value=f"Nombre: {role.name}\nID: {role.id}", inline=False)

        return embed

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rolelist", aliases=["rl", "list_roles", "rl_role", "rlrole"])
    async def list_roles(self, ctx):
        roles = ctx.guild.roles[1:]  # Excluye el rol @everyone
        role_menu = menus.MenuPages(RoleSelect(roles, per_page=10))
        await role_menu.start(ctx)

async def setup(bot):
    await bot.add_cog(Roles(bot)) 