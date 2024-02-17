import discord
from discord.ext import commands
from datetime import datetime
import pytz

class Date(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def date(self, ctx, continent, city):
        try:
            tz = pytz.timezone(f"{continent}/{city}")
            current_time = datetime.utcnow().astimezone(tz)
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            weekday = current_time.strftime("%A")
            utc_offset = tz.utcoffset(current_time).total_seconds() // 3600
            
            embed = discord.Embed(title="Current Date and Time", color=0x000000)
            embed.add_field(name="Continent", value=continent, inline=False)
            embed.add_field(name="City", value=city, inline=False)
            embed.add_field(name="Date and Time", value=formatted_time, inline=False)
            embed.add_field(name="Weekday", value=weekday, inline=False)
            embed.add_field(name="Time Difference from UTC", value=f"{utc_offset} hours", inline=False)
            
            await ctx.send(embed=embed)
        except pytz.UnknownTimeZoneError:
            await ctx.send("Could not find the specified time zone.")

async def setup(bot):
    await bot.add_cog(Date(bot))