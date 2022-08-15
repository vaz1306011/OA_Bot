import json
import random

import discord
from discord.ext import commands

from core.classes import Cog_Extension

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class React(Cog_Extension):
    @commands.command()  # N站指令
    async def nhentai(self, ctx):
        random_nhentai_digit = random.choice(jdata["nhentai"])
        await ctx.send(f"https://nhentai.net/g/{random_nhentai_digit}")

    @commands.command()  # 讓機器人說話指令
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()  # 清理訊息指令
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)

    @commands.command()
    async def test(self, ctx):
        await self.ctx_send(ctx, "red", "r")
        await self.ctx_send(ctx, "orange", "o")
        await self.ctx_send(ctx, "yellow", "y")
        await self.ctx_send(ctx, "green", "g")
        await self.ctx_send(ctx, "lightGreen", "lg")
        await self.ctx_send(ctx, "blue", "b")


def setup(bot):
    bot.add_cog(React(bot))
