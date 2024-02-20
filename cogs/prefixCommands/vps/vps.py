import discord
from discord.ext import commands
import asyncio
import json
import os

class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None

        self.data_folder = "Momo Data"
        os.makedirs(self.data_folder, exist_ok=True)
        self.config_file_path = os.path.join(self.data_folder, 'MomoInfoHost.json')

        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file_path, "r") as file:
                config = json.load(file)
                self.channel_id = config.get("channel_id")
        except FileNotFoundError:
            self.save_config()

    def save_config(self):
        config = {"channel_id": self.channel_id}
        with open(self.config_file_path, "w") as file:
            json.dump(config, file, indent=4)

    async def request_info(self, ctx):
        info = {}
        prompts = ["Mail", "Username", "First Name", "Last Name", "Password", "Name Server", "CPU", "RAM", "Disco", "Egg"]
        for prompt in prompts:
            embed = discord.Embed(title="Host Info", description=f"Please, fill {prompt}:")
            await ctx.send(embed=embed)
            try:
                response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
                info[prompt] = response.content
            except asyncio.TimeoutError:
                embed = discord.Embed(title="Host Info", description="Time out, please try again.")
                await ctx.send(embed=embed, delete_after=160)
                return None
        return info

    @commands.command(name="setuphost", aliases=["hCh"])
    @commands.has_permissions(administrator=True)
    async def setup_hostchannel(self, ctx, channel: discord.TextChannel):
        self.channel_id = channel.id
        self.save_config()
        embed = discord.Embed(title="Host Info", description=f"Channel successfully configured as {channel.mention} to send filled templates.")
        ctx.send(embed=embed, delete_after=160)

    @commands.command(name="request_hostInfo", aliases=["rHostI"])
    async def request_host_info(self, ctx):
        if self.channel_id is None:
            embed = discord.Embed(title="Host Info", description="Destination channel is not configured. Use `setuphost` command to configure it.")
            ctx.send(embed=embed, delete_after=160)
            return
        info = await self.request_info(ctx)
        if info:
            await self.send_host_template(ctx, info)

    async def send_host_template(self, ctx, info):
        template = self.build_template(info)
        canal_destino = ctx.guild.get_channel(self.channel_id)
        if canal_destino:
            message = await canal_destino.send(template)
            await message.add_reaction('✏️')
            self.bot.loop.create_task(self.wait_for_edit(ctx, message, info))

    async def wait_for_edit(self, ctx, message, info):
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✏️' and reaction.message.id == message.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
            if str(reaction.emoji) == '✏️':
                await message.clear_reactions()
                embed = discord.Embed( 
                    title="Host Info", 
                    description=
                    """ 
                        Plz indicate which field you want to edit (e.g., `Mail`) and the new value. 
                        Momo Usage: ``` Mail: <new value> \n Username: <new value> \nFirst Name: <new value> \n Last Name: <new value> \n Password: <new value> \n Name Server: <new value> \n CPU: <new value> \n RAM: <new value> \n Disco: <new value> \n Egg: <new value>```, 
                        Type 'done' when finished.
                    """
                ) 
                await ctx.send(embed=embed, delete_after=190)
 
                while True:
                    response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
                    if response.content.lower() == 'done':
                        break
  
                    parts = response.content.split(maxsplit=1)
                    if len(parts) == 2:
                        field_to_edit, new_value = parts
                        if field_to_edit in info:
                            info[field_to_edit] = new_value
                            await self.update_host_template(message, info)
                            embed = discord.Embed( title="Host Info", description=f"Field `{field_to_edit}` has been updated successfully. Any more edits? Type 'done' to finish." )
                            await ctx.send(embed=embed, delete_after=160)
                        else:
                            embed = discord.Embed(title="Host Info", description=f"Field `{field_to_edit}` is not valid. Try again or type 'done' to finish.")
                            await ctx.send( embed=embed, delete_after=160)
                    else:
                        embed = discord.Embed(title="Host Info", description="Incorrect format. Please indicate the field followed by the new value or type 'done' to finish.")
                        await ctx.send(embed=embed, delete_after=160)

        except asyncio.TimeoutError:
            await message.clear_reactions()
            embed = discord.Embed(title="Host Info", description="No changes were made.")
            await ctx.send(embed=embed, delete_after=160)

    async def update_host_template(self, message, info):
        updated_template = self.build_template(info)
        await message.edit(content=updated_template)

    def build_template(self, info):
        return f"""
# INFORMATION NECESSARY FOR HOSTING A SERVER
## **User: {info.get('Username')}**
- **Credentials:**
  - Mail: {info.get("Mail")}
  - Username: {info.get("Username")}
  - First Name: {info.get("First Name")}
  - Last Name: {info.get("Last Name")}
  - Password: {info.get("Password")}
- **Core Details:**
  - Server Name: {info.get("Name Server")}
- **Allocation Management:**
  - CPU: {info.get("CPU")}
  - RAM: {info.get("RAM")}
  - Disk: {info.get("Disco")}
- **Node:**
  - Egg (Bot language): {info.get("Egg")}
"""

async def setup(bot):
    await bot.add_cog(Host(bot))
