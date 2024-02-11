import os
import openai
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands

class GPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def call_gpt(self, prompt):
        headers = {
            "Content-Type": "Momo Data/Momojson",
            "Authorization": f"Bearer {os.getenv('MOMO_APIKEY')}"
        },
        data = {
            "model": "gpt-4-turbo-preview",  # Ajusta según el modelo deseado
            "prompt": prompt,
            "max_tokens": 50
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["text"]
        else:
            return "Error al llamar a la API de ChatGPT"

    @commands.command(name='gpt',aliases=["momo"])
    async def gpt_command(self, ctx, *, prompt: str):
        response = self.call_gpt(prompt)
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(GPT(bot))