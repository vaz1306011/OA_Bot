import asyncio
import json
import os

import discord
from discord.ext import commands

with open("data.json", "r", encoding="utf8") as jfile:
    data = json.load(jfile)
id_ = data["id"]
channel = data["channel"]

bot = commands.Bot(command_prefix="~", intents=discord.Intents.all())

cmds = []
for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        cmds.append(filename[:-3])


@bot.event
async def on_ready():
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # channel = bot.get_channel(channel["test-bot頻道"])
    # await channel.send("OA_Bot上線")
    print(f"[{now}] - OA_Bot上線")

    game = discord.Game(name="吸娜娜奇")
    await bot.change_presence(status=discord.Status.idle, activity=game)


async def load_extensions():
    for cmd in cmds:
        await bot.load_extension(f"cmds.{cmd}")


async def main():
    await load_extensions()
    await bot.start(data["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
