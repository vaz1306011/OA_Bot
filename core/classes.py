from discord.ext import commands

from core.data import DATA


class Cog_Extension(commands.Cog):
    DATA = DATA
    USER_ID: dict = DATA["user_id"]
    URL: dict = DATA["url"]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
