import discord    
from discord.ext import commands

class RoleSettings(commands.Cog, name="Settings"):  
    def __init__(self, bot):   
        self.bot = bot  
 
    @commands.command(name="createrole", aliases=["cr", "new_role", "newrole", "cr_role", "crrole"])
    async def role_creation(self, ctx, nombre_del_rol):
        if ctx.author.guild_permissions.manage_roles:
            guild = ctx.guild
            try:
                new_role = await guild.create_role(name=nombre_del_rol, color=discord.Color.blue())
                await ctx.send(f'Se ha creado el rol: {nombre_del_rol}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo crear el rol. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para crear roles.', delete_after=10)

    @commands.command(name="addperms", aliases=["ap", "add_perms", "ap_role", "aprole"])
    async def add_perms(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await role_mention.edit(permissions=discord.Permissions.all())
                await ctx.send(f'Se han agregado los permisos de {role_mention}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo agregar los permisos. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="listperms", aliases=["lp", "list_perms", "lp_role", "lprole", "mr"])
    async def list_perms(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            await ctx.send(f'Los permisos de {role_mention} son: {role_mention.permissions}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="giverole", aliases=["gr", "give_role", "gr_role", "grrole"])
    async def role_giver(self, ctx, member: discord.Member, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await member.add_roles(role_mention)
                await ctx.send(f'Se ha agregado el rol: {role_mention} al usuario: {member}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo agregar el rol. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="listroles", aliases=["lr", "list_role", "lr_role", "lrrole"])
    async def list_roles(self, ctx):
        if ctx.author.guild_permissions.manage_roles:
            guild = ctx.guild
            roles = guild.roles
            role_names = [role.name for role in roles]
            await ctx.send(f'Los nombres de los roles son: {", ".join(role_names)}', allowed_mentions=discord.AllowedMentions(replied_user=False), delete_after=20 )
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="changerole", aliases=["chr", "change_role", "chr_role", "chrrole"])
    async def role_changer(self, ctx, role_mention: discord.Role, *, nombre_del_rol):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await role_mention.edit(name=nombre_del_rol)
                await ctx.send(f'Se ha cambiado el nombre del rol: {role_mention}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo cambiar el nombre del rol. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="giveperms", aliases=["gp", "give_perms", "gp_role", "gprole"])
    async def give_perms(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await role_mention.edit(permissions=discord.Permissions.all())
                await ctx.send(f'Se han agregado los permisos de {role_mention}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo agregar los permisos. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="deleterole", aliases=["dr", "delete_role", "dr_role", "drrole"])
    async def role_deletion(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await role_mention.delete()
                await ctx.send(f'Se ha eliminado el rol: {role_mention}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo eliminar el rol. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="removerole", aliases=["rr", "remove_role", "rr_role", "rrrole"])
    async def role_removal(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await ctx.author.remove_roles(role_mention)
                await ctx.send(f'Se ha quitado el rol: {role_mention}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo quitar el rol. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="removeperms", aliases=["rp", "remove_perms", "rp_role", "rprole"])
    async def remove_perms(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await role_mention.edit(permissions=discord.Permissions.none())
                await ctx.send(f'Se han quitado los permisos de {role_mention}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo quitar los permisos. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)
            
    @commands.command(name="renamerole", aliases=["rnr", "rename_role", "rnr_role", "rnrole"])
    async def role_renaming(self, ctx, role_mention: discord.Role, *, nombre_del_rol):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await role_mention.edit(name=nombre_del_rol)
                await ctx.send(f'Se ha cambiado el nombre del rol: {role_mention}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo cambiar el nombre del rol. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="verifyrole", aliases=["vr", "verify_role", "vr_role", "vrrole"])
    async def verify_role(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            await ctx.send(f'Los permisos de {role_mention} son: {role_mention.permissions}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)
    
    @commands.command(name="unverifyrole", aliases=["ur", "unverify_role", "ur_role", "urrole"])
    async def unverify_role(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            await ctx.send(f'Los permisos de {role_mention} son: {role_mention.permissions}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="verifyperms", aliases=["vp", "verify_perms", "vp_role", "vprole"])
    async def verify_perms(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await role_mention.edit(permissions=discord.Permissions.all())
                await ctx.send(f'Se han agregado los permisos de {role_mention}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo agregar los permisos. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)

    @commands.command(name="unverifyperms", aliases=["up", "unverify_perms", "up_role", "uprole"])
    async def unverify_perms(self, ctx, role_mention: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            try:
                await role_mention.edit(permissions=discord.Permissions.none())
                await ctx.send(f'Se han quitado los permisos de {role_mention}', delete_after=10)
            except Exception as e:
                await ctx.send(f'No se pudo quitar los permisos. Error: {e}', delete_after=10)
        else:
            await ctx.send('No tienes los permisos necesarios para gestionar roles.', delete_after=10)


async def setup(bot):
    await bot.add_cog(RoleSettings(bot))