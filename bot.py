import asyncio
import os

import discord
from discord.ext.commands import Bot

token = os.environ.get("Discord Bot Token")

cmds = []
for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        cmds.append(filename[:-3])

bot = Bot(
    command_prefix="!",
    intents=discord.Intents.all(),
    description="老屁股機器人",
)


async def setup():
    for cmd in cmds:
        await bot.load_extension(f"cmds.{cmd}")

    await bot.start(token)


if __name__ == "__main__":
    try:
        asyncio.run(setup())

    except Exception as e:
        print(e)
        os.system("kill 1")
