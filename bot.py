import os  # for importing env vars for the bot to use
from tasklist import TaskList
from task import Task
from twitchio.ext import commands
from dotenv import load_dotenv
from typing import List

load_dotenv()
prefix = os.getenv("BOT_PREFIX")


class Bot(commands.Bot):

    def __init__(self):
        self.coworking_enabled: bool = False
        self.task_list: TaskList = TaskList()
        super().__init__(token=os.getenv("TMI_TOKEN"),
                         prefix=prefix,
                         initial_channels=[os.getenv("CHANNEL")])

    async def event_ready(self):
        # Log to console when bot is ready
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")
        print(f"Room is | {self.connected_channels}")
        await bot.connected_channels[0].send(f"Yes! Hello! I am here and ready to work, Vexcitement!")

    @commands.command()
    async def coworking(self, ctx: commands.Context) -> None:
        if ctx.author.is_broadcaster or ctx.author.is_mod:
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
        if self.coworking_enabled:
            new_task = Task(ctx.author.id, ctx.author.name, ctx.message.content[6:])

            if not self.task_list.task_exists(new_task):
                self.task_list.add_task(new_task)
                print(f'{ctx.author.name}, creating task "{new_task.task_desc}" for you.')
                await ctx.send(f'{ctx.author.name}, creating task "{new_task.task_desc}" for you.')
            else:
                print(f'{ctx.author.name}, the task "{new_task.task_desc}" already exists for you.')
                await ctx.send(f'{ctx.author.name}, the task "{new_task.task_desc}" already exists for you.')
        else:
            await ctx.send(f'{ctx.author.name}, coworking has not been enabled for this stream.')

    @commands.command()
    async def sidequest(self, ctx: commands.Context) -> None:
            if self.coworking_enabled:
                new_sidequest = Task(ctx.author.id, ctx.author.name, ctx.message.content[9:])

                if not self.task_list.task_exists(new_sidequest):
                    self.task_list.add_task(new_sidequest)
                    print(f'{ctx.author.name}, you have completed "{new_sidequest.task_desc}" as a sidequest.')
                    await ctx.send(f'{ctx.author.name}, you have completed "{new_sidequest.task_desc}" as a sidequest.')
                    self.task_list.mark_task_done(ctx.author)
                else:
                    print(f'{ctx.author.name}, the task "{new_sidequest.task_desc}" already exists for you.')
                    await ctx.send(f'{ctx.author.name}, the task "{new_sidequest.task_desc}" already exists for you.')
            else:
                await ctx.send(f'{ctx.author.name}, coworking has not been enabled for this stream.')

    @commands.command()
    async def edit(self, ctx: commands.Context) -> None:
        if self.coworking_enabled:
            if self.task_list.edit_current_task_desc(ctx.author, ctx.message.content):
                print(f'{ctx.author.name}, updated your active task to "{ctx.message.content[5:]}."')
                await ctx.send(f'{ctx.author.name}, updated your active task to "{ctx.message.content[5:]}."')
            else:
                print(
                    f'{ctx.author.name}, you have no active task to update. Create one with {prefix}task <description>')
                await ctx.send(f'{ctx.author.name}, you have no active task to update. Create one '
                               f'with {prefix}task <description>')
        else:
            await ctx.send(f'{ctx.author.name}, coworking has not been enabled for this stream.')

    @commands.command()
    async def delete(self, ctx: commands.Context) -> None:
        if self.coworking_enabled:
            if self.task_list.delete_active_task(ctx.author):
                print(f"{ctx.author.name}, deleted your active task. You may create a new one "
                      f"with {prefix}task <description>")
                await ctx.send(
                    f"{ctx.author.name}, deleted your active task. You may create a new one with {prefix}task "
                    f"<description>")
            else:
                print(
                    f'{ctx.author.name}, you have no active task to delete. Create one with {prefix}task <description>')
                await ctx.send(f'{ctx.author.name}, you have no active task to delete. Create '
                               f'one with {prefix}task <description>')
        else:
            await ctx.send(f'{ctx.author.name}, coworking has not been enabled for this stream.')

    @commands.command()
    async def current(self, ctx: commands.Context) -> None:
        if self.coworking_enabled:
            await ctx.send(self.task_list.get_current_task(ctx.author))
        else:
            await ctx.send(f'{ctx.author.name}, coworking has not been enabled for this stream.')

    @commands.command()
    async def time(self, ctx: commands.Context) -> None:
        if self.coworking_enabled:
            await ctx.send(self.task_list.get_accumulated_time(ctx.author))
        else:
            await ctx.send(f'{ctx.author.name}, coworking has not been enabled for this stream.')

    @commands.command()
    async def list(self, ctx: commands.Context) -> None:
        if self.coworking_enabled:
            message: str = f"{ctx.author.name}'s completed tasks: "
            completed_tasks: List[Task] = self.task_list.list_tasks(ctx.author)

            if len(completed_tasks) > 0:
                for task in completed_tasks:
                    message = message + f"{task.task_desc}, "
                message = message[:-2]
            else:
                message = f"{ctx.author.name}, you have no completed tasks. Create one with {prefix}task <description>"

            print({message})
            await ctx.send(message)
        else:
            await ctx.send(f'{ctx.author.name}, coworking has not been enabled for this stream.')

    @commands.command()
    async def done(self, ctx: commands.Context) -> None:
        if self.coworking_enabled:
            if self.task_list.mark_task_done(ctx.author):
                print(f"{ctx.author.name}, marking active task as done. Create one with {prefix}task <description>")
                await ctx.send(f"{ctx.author.name}, marking active task as done. Create "
                               f"one with {prefix}task <description>")
            else:
                print(
                    f'{ctx.author.name}, you have no active task to complete. Create one with {prefix}task '
                    f'<description>')
                await ctx.send(f'{ctx.author.name}, you have no active task to complete. Create one with '
                               f'{prefix}task <description>')
        else:
            await ctx.send(f'{ctx.author.name}, coworking has not been enabled for this stream.')


bot = Bot()
bot.run()