from discord.ext import commands

from core.classes import Cog_Extension
from core.tools import ctx_send


class Main(Cog_Extension):
    @commands.command()  # 顯示延遲指令
    async def ping(self, ctx):
        await ctx_send(ctx, f"{round(self.bot.latency*1000)}毫秒")


def setup(bot):
    print("已讀取Main")
    bot.add_cog(Main(bot))


def teardown(bot):
    print("已移除Main")
    bot.remove_cog("Main")
