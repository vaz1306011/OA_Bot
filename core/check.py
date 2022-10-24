import json

from discord.ext import commands

with open("data.json", "r", encoding="utf8") as jfile:
    data = json.load(jfile)

id = data["id"]
channel = data["channel"]


def is_owner():
    async def predicate(ctx):
        if ctx.author.id not in id["owner_ids"]:
            return False

        return True

    return commands.check(predicate)
