import discord
from discord.ext import commands
import json

class AutoBanner(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def autopfp(self, ctx, option: str = None, channel: discord.TextChannel = None):

        if option is None:
            embed = discord.Embed(title="autopfp command", description=f"This command can send banner pfp\n```Syntax: autopfp set/remove #channel\nExample: autopfp set #channel```")
            return await ctx.send(embed=embed)

        autopfp_db = self.load_autobanner_db()

        guild_id = str(ctx.guild.id)

        if option.lower() == "remove":
            autopfp_db.pop(guild_id, None)
            message = "remove"
        elif channel is not None:
            autopfp_db[channel.id] = guild_id
            message = f"{channel.name}"
        else:
            embed = discord.Embed(title="autopfp command", description=f"This command can send pfp\n```Syntax: autopfp set/remove #channel\nExample: autopfp set #channel```")
            return await ctx.send(embed=embed)

        self.save_autobanner_db(autopfp_db)
        embed = discord.Embed(title="", description=f"<a:MT_Weee:1158115648107458603> Current status autopfp `{message}` now.")
        await ctx.send(embed=embed)

    def load_autobanner_db(self):
        with open('autopfp.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_autobanner_db(self, autopfp_db):
        with open('autopfp.json', 'w', encoding='utf-8') as f:
            json.dump(autopfp_db, f, indent=4, ensure_ascii=False)

async def setup(bot):
    await bot.add_cog(AutoBanner(bot)) 
