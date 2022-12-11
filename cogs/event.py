import os
import random

import discord
import openai
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

        openai.api_key = os.environ.get("OPENAI_API_KEY")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        content = msg.content

        # 機器人判斷
        if msg.author.bot:
            return

        # 中獎判斷
        if random.randint(1, 10_000) == 1:
            await msg.channel.send("10000分之1的機率,被雷劈", reference=msg)

        if random.randint(1, 22_000_000) == 1:
            await msg.channel.send("2200萬分之一的機率,威力彩頭獎", reference=msg)

        # Sofia檢測
        if msg.author.id == self.id["Sofia"]:
            return

        # 指令判斷
        if content.startswith(self.bot.command_prefix):
            return

        # 關鍵字判斷
        if any(word in content for word in ("笑", "草", "ww")):
            word = random.choice(("笑死", "草", ""))
            await msg.channel.send(word + "w" * random.randint(2, 5))

        if "好" in content:
            await msg.channel.send("好耶")

        if any(word in content for word in ("確實", "雀石", "雀食")):
            word = random.choice(("確實", "雀石", "雀食"))
            await msg.channel.send(word)


async def setup(bot: commands.Bot):
    print("已讀取Event")
    await bot.add_cog(Event(bot))


async def teardown(bot: commands.Bot):
    print("已移除Event")
    await bot.remove_cog("Event")
