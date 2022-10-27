import random

import discord
from discord.ext import commands
from discord.ext.commands import Context

from core.check import is_owner, is_user
from core.classes import Cog_Extension
from core.tools import ctx_send


class React(Cog_Extension):
    @commands.command(brief="隨機產生6位數網址")  # N站指令
    async def nhentai(self, ctx: Context):
        random_nhentai_digit = random.choice(self.data["nhentai"])
        await ctx.send(f"https://nhentai.net/g/{random_nhentai_digit}")

    @commands.command(brief="讓機器人說話")  # 讓機器人說話指令
    async def say(self, ctx: Context, *, msg: str):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(brief="顯示小說下載雲端連結")  # 小說下載指令
    async def novel(self, ctx: Context):
        embed = discord.Embed(
            title="小說雲端網址",
            url=self.URL["novel"],
        )
        await ctx.send(embed=embed)

    @commands.command(brief="顯示自己id")
    async def myid(self, ctx: Context):
        await ctx_send(ctx, f"{ctx.author.id}")

    @commands.command(brief="清理訊息")  # 清理訊息指令
    @is_owner()
    async def cls(self, ctx: Context, num: int):
        await ctx.channel.purge(limit=num + 1)

    @commands.command(brief="顯示某人id")
    @is_owner()
    async def id(self, ctx: Context, member: discord.Member):
        await ctx_send(ctx, member.id)

    @commands.command(brief="顯示頻道id")
    @is_owner()
    async def channlid(self, ctx: Context):
        await ctx_send(ctx, f"{ctx.channel.id}")

    @commands.command(brief="顯示身分組id")
    @is_owner()
    async def roleid(self, ctx: Context, role: discord.Role):
        await ctx_send(ctx, f"{role.id}")

    @commands.command(brief="給定使用者身分組")
    @is_owner()
    async def addrole(
        self, ctx: Context, role: discord.Role, member: discord.Member | None = None
    ):
        member = member or ctx.message.author
        await member.add_roles(role)
        await ctx_send(ctx, f"已將 {member.mention} 移至 {role.mention} 身分組")

    @commands.command(brief="移除使用者身分組")
    @is_owner()
    async def removerole(
        self, ctx: Context, role: discord.Role, member: discord.Member | None = None
    ):
        member = member or ctx.message.author
        await member.remove_roles(role)
        await ctx_send(ctx, f"已將 {member.mention} 移出 {role.mention} 身分組")

    @commands.command(brief="猜拳")
    async def VOW(self, ctx: Context, *args):

        if len(args) == 1:
            n = int(args[0])
            if n >= 2:
                view = self.VOWView(n=n)

        elif len(args) >= 2:
            participant = [int(arg[2:-1]) for arg in args if is_user(arg)]
            view = self.VOWView(participant=participant)

        else:
            raise commands.BadArgument("請輸入使用者或人數")

        await ctx_send(ctx, "先別吵過來猜拳", view=view)

    @commands.command(brief="骰骰子")
    async def roll(self, ctx: Context, n: int | None = None, m: int | None = None):
        match n, m:
            case None, None:
                await ctx_send(ctx, f"骰出 {random.randint(1, 20)}")

            case n, None:
                await ctx_send(ctx, f"骰出 {random.randint(1, n)}")

            case n, m:
                await ctx_send(ctx, f"骰出 {random.randint(n, m)}")


async def setup(bot: commands.Bot):
    print("已讀取React")
    await bot.add_cog(React(bot))


async def teardown(bot: commands.Bot):
    print("已移除React")
    await bot.remove_cog("React")
