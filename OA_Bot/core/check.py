import re
from collections.abc import Iterable

import discord
from discord.ext.commands import Context

from OA_Bot.core.classes import Cog_Extension


async def is_owner(msg: Context | discord.Interaction):
    if isinstance(msg, Context):
        return msg.author.id in Cog_Extension.data.user_id.get("owner_ids", [])

    if isinstance(msg, discord.Interaction):
        return msg.user.id in Cog_Extension.data.user_id.get("owner_ids", [])


def is_user(name: str):
    return not not re.match(r"<@\d+>", name)


def is_role(name: str):
    return not not re.match(r"<@&\d+>", name)


def is_exception_content(message: discord.Message, command_prefix: object = None):
    # 機器人說的
    if message.author.bot:
        return True

    content = message.content

    # 指令
    if isinstance(command_prefix, str):
        return content.startswith(command_prefix)

    if isinstance(command_prefix, Iterable):
        prefixes = tuple(prefix for prefix in command_prefix if isinstance(prefix, str))
        return bool(prefixes) and content.startswith(prefixes)

    return False
