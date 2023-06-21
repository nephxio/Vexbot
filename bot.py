import os  # for importing env vars for the bot to use
from tasklist import TaskList
from task import Task
from twitchio.ext import commands
from dotenv import load_dotenv
from typing import List

load_dotenv()


class Bot(commands.Bot):

    def __init__(self):
        self.coworking_enabled: bool = False
        self.task_list: TaskList = TaskList()
        super().__init__(token=os.getenv("TMI_TOKEN"),
                         prefix=os.getenv("BOT_PREFIX"),
                         initial_channels=[os.getenv("CHANNEL")])

    async def event_ready(self):
        # Log to console when bot is ready
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")
        print(f"Room is | {self.connected_channels}")

    @commands.command()
    async def coworking(self, ctx: commands.Context) -> None:
        if ctx.author.is_broadcaster:
            if not self.coworking_enabled:
                self.coworking_enabled = True
                print(f"Coworking enabled, {ctx.author.name}")
                await ctx.send(f"Coworking enabled, {ctx.author.name}")
            else:
                self.coworking_enabled = False
                print(f"Coworking disabled, {ctx.author.name}")
                await ctx.send(f"Coworking disabled, {ctx.author.name}")

    @commands.command()
    async def task(self, ctx: commands.Context) -> None:
        new_task = Task(ctx.author.id, ctx.author.name, ctx.message.content)

        if not self.task_list.task_exists(new_task):
            self.task_list.add_task(new_task)
            print(f"{ctx.author.name}, creating task {new_task.task_desc} for you.")
            await ctx.send(f"{ctx.author.name}, creating task {new_task.task_desc} for you.")
        else:
            print(f'{ctx.author.name}, the task "{new_task.task_desc}" already exists for you.')
            await ctx.send(f'{ctx.author.name}, the task "{new_task.task_desc}" already exists for you.')

    @commands.command()
    async def edit(self, ctx: commands.Context) -> None:
        if self.task_list.edit_current_task_desc(ctx.author.id, ctx.message.content):
            print(f'{ctx.author.name}, updated your active task to "{ctx.message.content}."')
            await ctx.send(f'{ctx.author.name}, updated your active task to "{ctx.message.content}."')
        else:
            print(f'{ctx.author.name}, you have no active task to update. Create one with !task <description>')
            await ctx.send(f'{ctx.author.name}, you have no active task to update. Create one with !task <description>')

    @commands.command()
    async def delete(self, ctx: commands.Context) -> None:
        if self.task_list.delete_active_task(ctx.author.id):
            print(f"{ctx.author.name}, deleted your active task. You may create a new one with !task <description>")
            await ctx.send(f"{ctx.author.name}, deleted your active task. You may create a new one with !task "
                           f"<description>")
        else:
            print(f'{ctx.author.name}, you have no active task to delete. Create one with !task <description>')
            await ctx.send(f'{ctx.author.name}, you have no active task to delete. Create one with !task <description>')

    @commands.command()
    async def current(self, ctx: commands.Context) -> None:
        self.task_list.get_current_task(ctx.author)

    @commands.command()
    async def time(self, ctx: commands.Context) -> None:
        self.task_list.get_accumulated_time(ctx.author)

    @commands.command()
    async def list(self, ctx: commands.Context) -> None:
        message: str = f"{ctx.author.name}'s completed tasks: "
        completed_tasks: List[Task] = self.task_list.list_tasks(ctx.author)

        if len(completed_tasks) > 0:
            for task in completed_tasks:
                message = message + f"{task.task_desc}, "
            message = message[:-2]
        else:
            message = f"{ctx.author.name}, you have no completed tasks. Create one with !task <description>"

        print({message})
        await ctx.send(message)

    @commands.command()
    async def done(self, ctx: commands.Context) -> None:
        if self.task_list.mark_task_done(ctx.author):
            print(f"{ctx.author.name}, marking active task as done. Create one with !task <description>")
            await ctx.send(f"{ctx.author.name}, marking active task as done. Create one with !task <description>")
        else:
            print(f'{ctx.author.name}, you have no active task to complete. Create one with !task <description>')
            await ctx.send(f'{ctx.author.name}, you have no active task to complete. Create one with '
                           f'!task <description>')


bot = Bot()
bot.run()
