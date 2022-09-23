import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.tools import ctx_send


class Test(Cog_Extension):
    @commands.command()
    async def test(self, ctx):
        await ctx_send(ctx, "red", color="r")
        await ctx_send(ctx, "orange", color="o")
        await ctx_send(ctx, "yellow", color="y")
        await ctx_send(ctx, "green", color="g")
        await ctx_send(ctx, "lightGreen", color="lg")
        await ctx_send(ctx, "blue", color="b")

    @commands.command()
    async def test2(self, ctx):
        game = discord.Game(name="吸娜娜奇")
        await self.bot.change_presence(status=discord.Status.idle, activity=game)


async def setup(bot):
    print("已讀取Test")
    await bot.add_cog(Test(bot))


async def teardown(bot):
    print("已移除Test")
    await bot.remove_cog("Test")
