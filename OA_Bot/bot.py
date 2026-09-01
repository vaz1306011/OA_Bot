import asyncio
import glob
import os
from pathlib import Path
from typing import Optional, cast

import discord
from discord import app_commands
from discord.ext.commands import Bot
from dotenv import load_dotenv

from OA_Bot.core.tree import Tree

PACKAGE_DIR = Path(__file__).resolve().parent

load_dotenv()
token: str = cast(str, os.getenv("BOT_TOKEN"))
command_prefix = cast(str, os.getenv("COMMAND_PREFIX"))
cog_names = [
    cog[:-3]
    for cog in glob.glob("*.py", root_dir=PACKAGE_DIR / "cogs")
    if not cog.startswith("__")
]  # ["Cog1", "Cog2", "Cog3", ...]
COG_CHOICES = [app_commands.Choice(name=cog, value=cog) for cog in ["*", *cog_names]]


bot = Bot(
    command_prefix=command_prefix,
    help_command=None,
    intents=discord.Intents.all(),
    description="老屁股機器人",
    tree_cls=Tree,
)


async def setup(excludes: Optional[list[str]] = None):
    for cog in COG_CHOICES:
        if excludes and cog.value in excludes:
            continue
        if cog.value == "*":
            continue
        await bot.load_extension(f"OA_Bot.cogs.{cog.value}")

    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(setup(["ai"]))
