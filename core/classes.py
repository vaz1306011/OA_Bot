from discord.ext import commands

from core.data import DataClass


class Cog_Extension(commands.Cog):
    data = DataClass()
    # DATA = DATA
    # USER_ID: dict = DATA["user_id"]
    # URL: dict = DATA["url"]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data.update()
