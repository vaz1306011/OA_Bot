import json

import discord
from discord.ext import commands
from discord.ext.commands import Context

from core.tools import ctx_send_red

with open("data.json", "r", encoding="utf8") as jfile:
    data = json.load(jfile)

id = data["id"]
channel = data["channel"]


async def is_owner(msg: Context | discord.Interaction):
    if isinstance(msg, Context):
        await ctx_send_red(msg, "你沒有管理員權限")
        return msg.author.id in id["owner_ids"]

    if isinstance(msg, discord.Interaction):
        await msg.response.send_message("你沒有管理員權限", ephemeral=True)
        return msg.user.id in id["owner_ids"]


def is_user(name: str):
    return name.startswith("<@") and name[2] != "&" and name[-1] == ">"


def is_role(name: str):
    return name.startswith("<@&") and name[-1] == ">"


def on_message_exception(message: discord.Message):
    if message.author.bot:
        return True

    if message.channel.id == channel["ai問答"]:
        return True

    return False
