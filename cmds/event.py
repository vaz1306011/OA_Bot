import json

from discord.ext import commands

from core.classes import Cog_Extension
from core.tools import ctx_send

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class Event(Cog_Extension):
    @commands.Cog.listener()  # 成員加入公告
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(jdata["公告頻道"]))  # 設定頻道
        await channel.send(f"{member} 變成了老屁股")  # 發送訊息

    @commands.Cog.listener()  # 成員退出公告
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(int(jdata["公告頻道"]))
        await channel.send(f"{member} 不是老屁股了")

    @commands.Cog.listener()
    async def on_message(self, msg):
        content = msg.content

        if msg.author.bot:
            return

        if content.startswith(self.bot.command_prefix):
            return

        if "笑" in content:
            await msg.channel.send("笑死")

        if "好" in content:
            await msg.channel.send("好耶")

        if "確實" in content or "雀石" in content:
            await msg.channel.send("雀石")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        from functools import partial

        send = partial(ctx_send, ctx, color="red")
        if isinstance(error, commands.CommandNotFound):
            await send("指令不存在")
        elif isinstance(error, commands.MissingRequiredArgument):
            await send("缺少參數")
        elif isinstance(error, commands.MissingPermissions):
            await send("權限不足")
        elif isinstance(error, commands.CommandOnCooldown):
            await send("指令過於頻繁")
        elif isinstance(error, commands.CheckFailure):
            pass
        else:
            await ctx.send(str(error))


def setup(bot):
    print("已讀取Event")
    bot.add_cog(Event(bot))
