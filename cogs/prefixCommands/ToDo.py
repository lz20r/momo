import os
import json
import discord
from discord.ext import commands

class ToDo(commands.Cog):
    # Inicialización y diccionario de tareas
    def __init__(self, bot):
        self.bot = bot
        self.todos = {}

    # Comando para agregar una tarea
    @commands.command(name='addtodo', aliases=["atd"], help='Agrega una nueva tarea a tu lista TODO.')
    async def add_todo(self, ctx, *, task: str):
        user_id = ctx.author.id
        if user_id not in self.todos:
            self.todos[user_id] = []
        self.todos[user_id].append(task)
        await ctx.send(f'Tarea agregada: "{task}"')

    # Comando para listar todas las tareas
    @commands.command(name='listtodo', aliases=["lstd"], help='Lista todas tus tareas pendientes.')
    async def list_todo(self, ctx):
        user_id = ctx.author.id
        tasks = self.todos.get(user_id, [])
        if not tasks:
            await ctx.send('No tienes tareas pendientes.')
            return
        response = "Tus tareas pendientes son:\n" + "\n".join(f"{i+1}. {task}" for i, task in enumerate(tasks))
        await ctx.send(response)

    # Comando para eliminar una tarea
    @commands.command(name='deltodo', aliases=["dtd"], help='Elimina una tarea de tu lista TODO por su número.')
    async def delete_todo(self, ctx, task_number: int):
        user_id = ctx.author.id
        if user_id in self.todos and 0 < task_number <= len(self.todos[user_id]):
            removed_task = self.todos[user_id].pop(task_number - 1)
            await ctx.send(f'Tarea eliminada: "{removed_task}"')
        else:
            await ctx.send('Número de tarea no válido.')

async def setup(bot):
    await bot.add_cog(ToDo(bot))