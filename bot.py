import asyncio
import os

import discord
from discord.ext.commands import Bot

token = os.environ.get("OA_BOT_TOKEN")

cogs = []
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        cogs.append(filename[:-3])

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
