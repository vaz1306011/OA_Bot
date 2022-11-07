import json

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

with open("data.json", "r", encoding="utf8") as jfile:
    data = json.load(jfile)

id = data["id"]
channel = data["channel"]


def is_owner_ctx():
    async def predicate(ctx: Context):
        return ctx.author.id in id["owner_ids"]

    return commands.check(predicate)


def is_owner_interaction():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.id in id["owner_ids"]

    return app_commands.check(predicate)


def is_user(name: str):
    return name.startswith("<@") and name[2] != "&" and name[-1] == ">"


def is_role(name: str):
    return name.startswith("<@&") and name[-1] == ">"
