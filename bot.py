import asyncio
import glob
import os

import discord
from discord.ext.commands import Bot

token = os.environ.get("OA_BOT_TOKEN")

cogs = glob.glob("*.py", root_dir="cogs")
cogs = list(map(lambda x: x[:-3], cogs))

bot = Bot(
    command_prefix="!",
    intents=discord.Intents.all(),
    description="老屁股機器人",
)


async def setup():
    for cog in cogs:
        await bot.load_extension(f"cogs.{cog}")

    await bot.start(token)


if __name__ == "__main__":
    try:
        asyncio.run(setup())
    except Exception as e:
        print(e)
        os.system("kill 1")
