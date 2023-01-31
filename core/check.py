import re

import discord
from discord.ext.commands import Context

from bot import bot
from core.data import USER_ID
from core.tools import ctx_send_red


async def is_owner(msg: Context | discord.Interaction):
    if isinstance(msg, Context):
        if not msg.author.id in USER_ID["owner_ids"]:
            await ctx_send_red(msg, "你沒有管理員權限")
            return False
        return True

    if isinstance(msg, discord.Interaction):
        if not msg.user.id in USER_ID["owner_ids"]:
            await msg.response.send_message("你沒有管理員權限", ephemeral=True)
            return False
        return True


def is_user(name: str):
    return not not re.match(r"<@\d+>", name)


def is_role(name: str):
    return not not re.match(r"<@&\d+>", name)


def is_exception_content(message: discord.Message):
    # 機器人說的
    if message.author.bot:
        return True

    content = message.content

    # 指令
    if content.startswith(bot.command_prefix):
        return True

    return False
