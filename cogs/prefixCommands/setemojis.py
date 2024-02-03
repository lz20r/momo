import aiohttp
import discord
from discord.ext import commands
from discord import utils, Emoji, PartialEmoji   


class EmojiSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
 
    @commands.command(name="addmoremoji", aliases=["ae", "add_emoji", "ae_emoji", "aeemoji"]) 
    @commands.has_permissions(manage_emojis=True)
    async def add_emoji(self, ctx, *emoji_urls):
        added_emojis = []
        
        if not emoji_urls:
            embed = discord.Embed(description=f"{ctx.author} you need to provide the emoji to wanna add.", color=discord.Color.red())
            return await ctx.send(embed=embed,  delete_after=10)
        
        for emoji_url in emoji_urls:
            try:
                emoji_info = discord.PartialEmoji.from_str(emoji_url)

                if emoji_info.id:
                    extension = '.gif' if emoji_info.animated else '.png'
                    url = f'https://cdn.discordapp.com/emojis/{emoji_info.id}{extension}'

                    async with ctx.typing():
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as response:
                                emoji_image = await response.read()
                                
                    emoji = await ctx.guild.create_custom_emoji(name=emoji_info.name, image=emoji_image) 
                    added_emojis.append(str(emoji))
                else:
                    embed = discord.Embed(description=f"{ctx.author} {emoji_info} is not a valid emoji.", color=discord.Color.red()) 
                    return await ctx.send(embed=embed,  delete_after=10)
            except ValueError as e:
                embed = discord.Embed(description=f"{ctx.author} Error: ```{e}```", color=discord.Color.red())
                added_emojis.append(ctx.send(embed=embed, delete_after=10))
                
            if added_emojis: 
                embed = discord.Embed(title="", description=f"{ctx.author} had already added: {', '.join(added_emojis)} to the server {ctx.guild} correctly", color=discord.Color.green()) 
                await ctx.send(embed=embed, delete_after=10)
            else:
                embed = discord.Embed(title="", description=f"{ctx.author} you need to provide the emoji to add.", color=discord.Color.red(), delete_after=10)
                return await ctx.send(embed=embed, delete_after=10) 
    
    @commands.command(name="deleteemoji", aliases=["de", "delete_emoji", "de_emoji", "deemoji"])
    @commands.has_permissions(manage_emojis=True)
    async def delete_emoji(self, ctx, emoji_name_or_id):
        emoji_by_name = discord.utils.get(ctx.guild.emojis, name=emoji_name_or_id)

        emoji_by_id = None
        try:
            emoji_id = int(emoji_name_or_id, 30)
            emoji_by_id = discord.utils.get(ctx.guild.emojis, id=emoji_id)
        except ValueError:
            pass

        if emoji_by_name:
            await emoji_by_name.delete()
            await ctx.send(f'{ctx.author} personalized emoji {emoji_by_name.name} deleted.')
        elif emoji_by_id:
            await emoji_by_id.delete()
            await ctx.send(f'{ctx.author} Personalized emoji  {emoji_by_id.id} deleted.')
        else:
            await ctx.send(f'{ctx.author} Personalized emoji {emoji_name_or_id} not found.')

async def setup(bot):
    await bot.add_cog(EmojiSettings(bot)) 
