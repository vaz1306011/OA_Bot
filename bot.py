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

bot = Bot(command_prefix="!", intents=discord.Intents.all(), description="老屁股機器人")


@bot.event
async def on_ready():
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] - OA_Bot上線")

    game = discord.Game(name="吸娜娜奇")
    await bot.change_presence(status=discord.Status.idle, activity=game)


async def setup():
    for cmd in cmds:
        await bot.load_extension(f"cmds.{cmd}")

    await bot.start(token)


if __name__ == "__main__":
    try:
        asyncio.run(setup())

    except:
        os.system("kill 1")
