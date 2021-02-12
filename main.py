import asyncio
from pathlib import Path
import discord
from discord.ext import commands
from time import gmtime, strftime
import time

async def run():
    bot = Bot(description="Bot description")
    try:
        await bot.start("TOKEN")
    except KeyboardInterrupt:
        await bot.logout()

class Bot(commands.Bot):

    def __init__(self, **kwargs):
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            description=kwargs.pop('description'),
            intents=intents
        )
        self.loop.create_task(self.load_all_extensions())

    def logger(self, type, text):
        if type == "INFO":
            print(f"[INFO] {text}")
        elif type == "WARN":
            print(f"[WARN] {text}")
        elif type == "ERROR":
            print(f"[ERROR] {text}")

    async def load_all_extensions(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Discord"))
        await asyncio.sleep(1)
        cogs = [x.stem for x in Path('cogs').glob('*.py')]
        for extension in cogs:
            try:
                self.load_extension(f'cogs.{extension}')
                self.logger("INFO", f"{extension} was loaded.")
            except Exception as e:
                self.logger("ERROR", f"{extension} failed to load.\n{e}")
        try:
            self.load_extension(f'jishaku')
            self.logger("INFO", f"Jishaku was loaded.")
        except Exception as e:
            self.logger("ERROR", f"Jishaku failed to load.\n{e}")

    async def on_ready(self):
        am_pm = time.strftime("%p", time.gmtime())
        if am_pm == "AM":
            self.logger("INFO", "Good Morning Harry! I am alive and awake.")
        else:
            self.logger("INFO", "Good Afternoon Harry! I want to sleep - but I am alive.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())