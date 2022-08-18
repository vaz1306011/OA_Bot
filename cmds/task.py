import asyncio
import json

from core.classes import Cog_Extension

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def interval():  # 間隔時間公告
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(jdata["test-bot頻道"])
            while not self.bot.is_closed():
                await self.channel.send("")
                await asyncio.sleep(5)

        # self.bg_task = self.bot.loop.create_task(interval())


def setup(bot):
    print("已讀取Task")
    bot.add_cog(Task(bot))


def teardown(bot):
    print("已移除Task")
    bot.remove_cog("Task")
