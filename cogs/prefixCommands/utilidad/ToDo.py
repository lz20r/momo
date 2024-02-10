import discord
from discord.ext import commands
import json
import os
from datetime import datetime

class ToDo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = os.path.join('Momo Data', 'MomoListUsers')
        os.makedirs(self.data_folder, exist_ok=True)  # Crea la estructura de carpetas si no existe
        self.data_file = os.path.join(self.data_folder, 'MomoListToDo.json')
        self.todos = self.load_todos()

    def load_todos(self):
        if os.path.isfile(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_todos(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.todos, f, indent=4)

    @commands.command(name='addtodo', aliases=["atd"], help='Agrega una nueva tarea a tu lista TODO o a la de un usuario mencionado.')
    async def add_todo(self, ctx, member: discord.Member = None, *, task: str):
        target_user = member if member else ctx.author
        user_id = str(target_user.id)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_short = datetime.now().strftime("%d/%m/%Y")
        if user_id not in self.todos:
            self.todos[user_id] = {'name': target_user.name, 'created': date_short, 'tasks': []}
        self.todos[user_id]['tasks'].append({'task': task, 'timestamp': timestamp, 'completed': False})
        self.save_todos()

        confirmation_msg = f'Tarea "{task}" agregada a la lista de {target_user.display_name}.'
        await ctx.send(confirmation_msg)

    @commands.command(name='listtodo', aliases=["lstd"], help='Lista todas tus tareas pendientes o las de un usuario mencionado.')
    async def list_todo(self, ctx, member: discord.Member = None):
        target_user = member if member else ctx.author
        user_id = str(target_user.id)
        user_data = self.todos.get(user_id, {})
        tasks = user_data.get('tasks', [])
        
        if not tasks:
            response = f'{target_user.display_name} no tiene tareas pendientes.'
            await ctx.send(response)
            return

        response = f"Tareas pendientes de {user_data.get('name')} (Creado el {user_data.get('created')}):\n"
        for i, task in enumerate(tasks):
            checkbox = ":white_check_mark:" if task['completed'] else ":x:"
            response += f"{i+1}. {task['task']} {checkbox} (Añadido el {task['timestamp']})\n"
        await ctx.send(response)

    @commands.command(name='edittodo', aliases=["etd"], help='Edita una tarea de tu lista TODO por su número.')
    async def edit_todo(self, ctx, task_number: int, *, new_task: str):
        user_id = str(ctx.author.id)
        if user_id in self.todos and 0 < task_number <= len(self.todos[user_id]['tasks']):
            self.todos[user_id]['tasks'][task_number - 1]['task'] = new_task
            self.save_todos()
            await ctx.send(f'Tarea editada: "{new_task}"')
        else:
            await ctx.send('Número de tarea no válido.')

    @commands.command(name='completetodo', aliases=["ctd"], help='Marca una tarea como completada por su número.')
    async def complete_todo(self, ctx, task_number: int):
        user_id = str(ctx.author.id)
        if user_id in self.todos and 0 < task_number <= len(self.todos[user_id]['tasks']):
            self.todos[user_id]['tasks'][task_number - 1]['completed'] = True
            self.save_todos()
            await ctx.send(f'Tarea marcada como completada.')
        else:
            await ctx.send('Número de tarea no válido.') 
            
    @commands.command(name='deltodo', aliases=["dtd"], help='Elimina una tarea de tu lista TODO por su número.')
    async def delete_todo(self, ctx, task_number: int):
        user_id = str(ctx.author.id)
        if user_id in self.todos and 0 < task_number <= len(self.todos[user_id]['tasks']):
            removed_task = self.todos[user_id]['tasks'].pop(task_number - 1)['task']
            self.save_todos()
            await ctx.send(f'Tarea eliminada: "{removed_task}"')
        else:
            await ctx.send('Número de tarea no válido.')

async def setup(bot):
    await bot.add_cog(ToDo(bot))
