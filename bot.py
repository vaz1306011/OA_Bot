import asyncio
import json
import os

import discord
from discord.ext.commands import Bot

with open("data.json", "r", encoding="utf8") as jfile:
    data = json.load(jfile)

token = data["TOKEN"]

cmds = []
for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        cmds.append(filename[:-3])

bot = Bot(
    command_prefix="!",
    intents=discord.Intents.all(),
    description="老屁股機器人",
    application_id="799467265010565120",
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
