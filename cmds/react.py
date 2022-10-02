import random

from discord import Member, Role, User
from discord.ext import commands
from discord.ext.commands import Context

from core.check import is_owner
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

    @commands.command(brief="清理訊息")  # 清理訊息指令
    @is_owner()
    async def clean(self, ctx: Context, num: int):
        await ctx.channel.purge(limit=num + 1)

    @commands.command(brief="顯示某人id")
    @is_owner()
    async def id(self, ctx: Context, user: User):
        await ctx_send(ctx, user.id)

    @commands.command(brief="顯示自己id")
    async def myid(self, ctx: Context):
        await ctx_send(ctx, f"{ctx.author.id}")

    @commands.command(brief="顯示頻道id")
    @is_owner()
    async def channlid(self, ctx: Context):
        await ctx_send(ctx, f"{ctx.channel.id}")

    @commands.command(brief="顯示身分組id")
    @is_owner()
    async def roleid(self, ctx: Context, role: Role):
        await ctx_send(ctx, f"{role.id}")

    @commands.command(brief="給定使用者身分組")
    @is_owner()
    async def addrole(self, ctx: Context, role: Role, member: Member = None):
        member = member or ctx.message.author
        await member.add_roles(role)
        await ctx_send(ctx, f"已將 {member.mention} 移至 {role.mention} 身分組")

    @commands.command(brief="移除使用者身分組")
    @is_owner()
    async def removerole(self, ctx: Context, role: Role, member: Member = None):
        member = member or ctx.message.author
        await member.remove_roles(role)
        await ctx_send(ctx, f"已將 {member.mention} 移出 {role.mention} 身分組")


async def setup(bot: commands.Bot):
    print("已讀取React")
    await bot.add_cog(React(bot))


async def teardown(bot: commands.Bot):
    print("已移除React")
    await bot.remove_cog("React")
