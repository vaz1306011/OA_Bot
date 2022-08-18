import json
import random

from discord.ext import commands

from core.check import is_owner
from core.classes import Cog_Extension
from core.tools import ctx_send

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
    @is_owner()
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)

    @commands.command()
    @is_owner()
    async def myid(self, ctx):
        await ctx.send(f"{ctx.author.id}")

    @commands.command()
    @is_owner()
    async def channlid(self, ctx):
        await ctx.send(f"{ctx.channel.id}")

    @commands.command()
    async def test(self, ctx):
        await ctx_send(ctx, "red", "r")
        await ctx_send(ctx, "orange", "o")
        await ctx_send(ctx, "yellow", "y")
        await ctx_send(ctx, "green", "g")
        await ctx_send(ctx, "lightGreen", "lg")
        await ctx_send(ctx, "blue", "b")


def setup(bot):
    print("已讀取React")
    bot.add_cog(React(bot))


def teardown(bot):
    print("已移除React")
    bot.remove_cog("React")
