from discord.ext import commands

from OA_Bot.core.data import DataClass


class Cog_Extension(commands.Cog):
    data = DataClass.load()
    # DATA = DATA
    # USER_ID: dict = DATA["user_id"]
    # URL: dict = DATA["url"]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_exception_content(self, message):
        from OA_Bot.core.check import is_exception_content

        return is_exception_content(message, self.bot.command_prefix)
