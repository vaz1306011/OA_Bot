import random

import discord
from discord.ext import commands

from core.check import is_owner
from core.classes import Cog_Extension
from core.tools import ctx_send


class React(Cog_Extension):
    @commands.command(brief="隨機產生6位數網址")  # N站指令
    async def nhentai(self, ctx):
        random_nhentai_digit = random.choice(self.data["nhentai"])
        await ctx.send(f"https://nhentai.net/g/{random_nhentai_digit}")

    @commands.command(brief="讓機器人說話")  # 讓機器人說話指令
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(brief="清理訊息")  # 清理訊息指令
    @is_owner()
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)

    @commands.command(brief="顯示某人id")
    @is_owner()
    async def id(self, ctx, user: discord.User):
        await ctx_send(ctx, user.id)

    @commands.command(brief="顯示使用者id")
    @is_owner()
    async def myid(self, ctx):
        await ctx_send(ctx, f"{ctx.author.id}")

    @commands.command(brief="顯示頻道id")
    @is_owner()
    async def channlid(self, ctx):
        await ctx_send(ctx, f"{ctx.channel.id}")


def setup(bot):
    print("已讀取React")
    bot.add_cog(React(bot))


def teardown(bot):
    print("已移除React")
    bot.remove_cog("React")
