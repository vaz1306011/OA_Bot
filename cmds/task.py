import asyncio

import discord
from discord.ext import commands

from core.classes import Cog_Extension


class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def interval():  # 間隔時間公告
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(self.channel["test-bot頻道"])
            while not self.bot.is_closed():
                await self.channel.send("")
                await asyncio.sleep(5)

        # self.bg_task = self.bot.loop.create_task(interval())


async def setup(bot):
    print("已讀取Task")
    await bot.add_cog(Task(bot))


async def teardown(bot):
    print("已移除Task")
    await bot.remove_cog("Task")
