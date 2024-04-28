from discord.ext import commands

from core.classes import Cog_Extension
from core.logger import logger


class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # async def interval():  # 間隔時間公告
        #     await self.bot.wait_until_ready()
        #     self.channels = self.bot.get_channel(self.channels["test-bot"])
        #     while not self.bot.is_closed():
        #         await self.channels.send("")
        #         await asyncio.sleep(5)

        # self.bg_task = self.bot.loop.create_task(interval())


async def setup(bot: commands.Bot):
    await bot.add_cog(Task(bot))
    logger.info("已讀取 Task 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("Task")
    logger.info("已移除 Task 模塊")
