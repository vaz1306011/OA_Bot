import json

from discord.ext import commands

from core.tools import ctx_send

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


def is_owner():
    async def predicate(ctx):
        if ctx.author.id not in jdata["owner_ids"]:
            await ctx_send(ctx, "權限不足", "r")
            return False
        return True

    return commands.check(predicate)
