import json

from discord.ext import commands


class Cog_Extension(commands.Cog):
    with open("data.json", "r", encoding="utf8") as f:
        data = json.load(f)

    id: dict = data["id"]
    role: dict = data["role"]
    channel: dict = data["channel"]
    guild: dict = data["guild"]
    URL: dict = data["URL"]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
