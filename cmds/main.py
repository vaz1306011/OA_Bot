import discord
from discord.ext import commands

from bot import cmds
from core.check import is_owner
from core.classes import Cog_Extension
from core.tools import ctx_send


class Main(Cog_Extension):
    @commands.command(brief="載入模塊")
    @is_owner()
    async def load(self, ctx, extension):
        await self.bot.load_extension(f"cmds.{extension}")
        await ctx_send(ctx, f"已載入{extension}")

    @commands.command(brief="卸載模塊")
    @is_owner()
    async def unload(self, ctx, extension):
        await self.bot.unload_extension(f"cmds.{extension}")
        await ctx_send(ctx, f"已卸載{extension}")

    @commands.command(brief="重新載入模塊")
    @is_owner()
    async def reload(self, ctx, *extensions):
        if "*" in extensions:
            for cmd in cmds:
                await self.bot.unload_extension(f"cmds.{cmd}")
                await self.bot.load_extension(f"cmds.{cmd}")
                await ctx_send(ctx, f"已重新載入{cmd}")
            await ctx.channel.purge(limit=len(cmds))
            await ctx_send(ctx, "已重新載入所有指令")
        else:
            extensions = set(extensions)
            error_list = set()
            for extension in extensions:
                try:
                    await self.bot.reload_extension(f"cmds.{extension}")
                    await ctx_send(ctx, f"已重新載入{extension}")
                except commands.ExtensionNotLoaded:
                    error_list.add(extension)
                    await ctx_send(ctx, f"<{extension}不存在或無法載入>")

            extensions_len = len(extensions)
            if extensions_len > 1:
                extensions = extensions - error_list
                await ctx.channel.purge(limit=extensions_len)
                reload_msg = f"已重新載入{', '.join(extensions)}    " if extensions else ""
                cant_reload_msg = (
                    ("<" + ", ".join(error_list) + "無法載入>") if error_list else ""
                )
                await ctx_send(ctx, f"{reload_msg}{cant_reload_msg}")

    @commands.command(brief='設置機器人狀態')
    @is_owner()
    async def set_status(self, ctx, status):
        match status:
            case "online":
                await ctx.bot.change_presence(status=discord.Status.online)
                await ctx_send(ctx, "已更改狀態為: 在線")
            case "idle":
                await ctx.bot.change_presence(status=discord.Status.idle)
                await ctx_send(ctx, "已更改狀態為: 空閒")
            case "dnd":
                await ctx.bot.change_presence(status=discord.Status.dnd)
                await ctx_send(ctx, "已更改狀態為: 忙碌")
            case "offline":
                await ctx.bot.change_presence(status=discord.Status.offline)
                await ctx_send(ctx, "已更改狀態為: 離線")
            case _:
                raise commands.BadArgument("無效的狀態")

    @commands.command(brief="顯示ping值")  # 顯示延遲指令
    async def ping(self, ctx):
        await ctx_send(ctx, f"{round(self.bot.latency*1000)}毫秒")


async def setup(bot):
    print("已讀取Main")
    await bot.add_cog(Main(bot))


async def teardown(bot):
    print("已移除Main")
    await bot.remove_cog("Main")
