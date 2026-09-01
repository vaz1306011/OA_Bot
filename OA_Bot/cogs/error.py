from discord.ext import commands
from discord.ext.commands import Context

from OA_Bot.core.classes import Cog_Extension
from OA_Bot.core.logger import logger


class Error(Cog_Extension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception):
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Error(bot))
    logger.info("已讀取 Error 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("Error")
    logger.info("已移除 Error 模塊")
