import asyncio
import enum
import glob
import os

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN")
__cogs = glob.glob("*.py", root_dir="cogs")
__cogs = list(map(lambda x: x[:-3], __cogs))
CogType = enum.Enum("Cog", {cog: cog for cog in (["*"] + __cogs)})


bot = Bot(
    command_prefix="$",
    help_command=None,
    intents=discord.Intents.all(),
    description="老屁股機器人",
)


async def setup():
    for cog in CogType:
        if cog.name == "*":
            continue
        await bot.load_extension(f"cogs.{cog.name}")

    await bot.start(token)


if __name__ == "__main__":
    # try:
    asyncio.run(setup())
    # except Exception as e:
    #     print(e)
    #     os.system("kill 1")
