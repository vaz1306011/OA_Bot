import json
import os

import discord
from discord.ext import commands

with open("setting.json", "r", encoding="utf8") as jfile:
    data = json.load(jfile)

bot = commands.Bot(command_prefix="~")

cmds = []
for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        cmds.append(filename[:-3])


@bot.event
async def on_ready():
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # channel = bot.get_channel(jdata["test-bot頻道"])
    # await channel.send("OA_Bot上線")
    print(f"[{now}] - OA_Bot上線")

    game = discord.Game(name="吸娜娜奇")
    await bot.change_presence(status=discord.Status.idle, activity=game)


if __name__ == "__main__":
    for cmd in cmds:
        bot.load_extension(f"cmds.{cmd}")

    bot.run(data["TOKEN"])
