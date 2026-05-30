import asyncio
import enum
import glob
import os
from pathlib import Path

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

PACKAGE_DIR = Path(__file__).resolve().parent

load_dotenv()
token = os.getenv("BOT_TOKEN")
command_prefix = os.getenv("COMMAND_PREFIX")
__cogs = [
    cog[:-3]
    for cog in glob.glob("*.py", root_dir=PACKAGE_DIR / "cogs")
    if not cog.startswith("__")
]  # ["Cog1", "Cog2", "Cog3", ...]
CogType = enum.Enum("Cog", {cog: cog for cog in (["*"] + __cogs)})


bot = Bot(
    command_prefix=command_prefix,
    help_command=None,
    intents=discord.Intents.all(),
    description="老屁股機器人",
)


async def setup(excludes: list[str] = None):
    for cog in CogType:
        if excludes and cog.name in excludes:
            continue
        if cog.name == "*":
            continue
        await bot.load_extension(f"OA_Bot.cogs.{cog.name}")

    await bot.start(token)


if __name__ == "__main__":
    # try:
    asyncio.run(setup(["ai"]))
    # except Exception as e:
    #     print(e)
    #     os.system("kill 1")
