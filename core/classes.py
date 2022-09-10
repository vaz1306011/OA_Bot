import json

from discord.ext import commands


class Cog_Extension(commands.Cog):
    with open("data.json", "r", encoding="utf8") as f:
        data = json.load(f)
    id_ = data["id"]
    channel = data["channel"]

    def __init__(self, bot):
        self.bot = bot
