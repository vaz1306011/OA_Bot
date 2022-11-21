import random

import discord
from discord.ext import commands

from core.classes import Cog_Extension


class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] - OA_Bot上線")

        game = discord.Game(name="吸娜娜奇")
        await self.bot.change_presence(status=discord.Status.idle, activity=game)

    @commands.Cog.listener()  # 成員加入公告
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(self.channel["公告頻道"])  # 設定頻道
        await channel.send(f"{member.mention} 變成了老屁股")  # 發送訊息

    @commands.Cog.listener()  # 成員退出公告
    async def on_member_remove(self, member: discord.Member):
        channel = self.bot.get_channel(self.channel["公告頻道"])
        await channel.send(f"{member.mention} 不是老屁股了")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        content = msg.content

        if msg.author.bot:
            return

        if random.randint(1, 10_000) == 1:
            await msg.channel.send("10000分之1的機率,被雷劈")

        if random.randint(1, 22_000_000) == 1:
            await msg.channel.send("2200萬分之一的機率,威力彩頭獎")

        # Sofia檢測
        if msg.author.id == self.id["Sofia"]:
            return

        if content.startswith(self.bot.command_prefix):
            return

        if "笑" in content:
            await msg.channel.send("笑死")

        if "好" in content:
            await msg.channel.send("好耶")

        if "確實" in content or "雀石" in content:
            await msg.channel.send("雀石")


async def setup(bot: commands.Bot):
    print("已讀取Event")
    await bot.add_cog(Event(bot))


async def teardown(bot: commands.Bot):
    print("已移除Event")
    await bot.remove_cog("Event")
