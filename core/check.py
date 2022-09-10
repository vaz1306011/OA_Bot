import json

from discord.ext import commands

from core.tools import ctx_send

with open("data.json", "r", encoding="utf8") as jfile:
    data = json.load(jfile)
id_ = data["id"]
channel = data["channel"]


def is_owner():
    async def predicate(ctx):
        if ctx.author.id not in id_["owner_ids"]:
            await ctx_send(ctx, "權限不足", "r")
            return False
        return True

    return commands.check(predicate)
