import os  # for importing env vars for the bot to use
from twitchio.ext import commands
from dotenv import load_dotenv

load_dotenv()


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=os.getenv("TMI_TOKEN"),
                         prefix=os.getenv("BOT_PREFIX"),
                         initial_channels=[os.getenv("CHANNEL")])

    async def event_ready(self):
        # Log to console when bot is ready
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")
        print(f"Room is | {self.connected_channels}")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"Hello {ctx.author.name}")

bot = Bot()
bot.run()
