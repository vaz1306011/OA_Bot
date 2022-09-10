import discord
from discord.ext import commands

from core.classes import Cog_Extension
from core.tools import ctx_send


class Event(Cog_Extension):
    @commands.Cog.listener()  # 成員加入公告
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.channel["公告頻道"])  # 設定頻道
        await channel.send(f"{member} 變成了老屁股")  # 發送訊息

    @commands.Cog.listener()  # 成員退出公告
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(self.channel["公告頻道"])
        await channel.send(f"{member} 不是老屁股了")

    @commands.Cog.listener()
    async def on_message(self, msg):
        content = msg.content

        if msg.author.bot:
            return

        # Sofia檢測
        if msg.author.id == self.id_["Sofia"]:
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
    async def on_command_error(self, ctx, error: Exception):
        from functools import partial

        send = partial(ctx_send, ctx, color="red")

        try:
            raise error
        except commands.CommandNotFound as e:
            await send(f"指令不存在 <{e}>")
        except commands.MissingRequiredArgument as e:
            await send(f"缺少參數 <{e}>")
        except commands.BadArgument as e:
            await send(f"參數錯誤 <{e}>")
        except commands.MissingPermissions as e:
            await send(f"權限不足 <{e}>")
        except commands.CheckFailure as e:
            await send(f"檢查失敗 <{e}>")
        except commands.CommandOnCooldown as e:
            await send(f"指令過於頻繁 <{e}>")
        except commands.CommandInvokeError as e:
            await send(f"指令執行錯誤 <{e}>")
        except commands.CommandError as e:
            await send(f"指令錯誤 <{e}>")
        except Exception as e:
            await send(f"發生錯誤 <{e}>")


def setup(bot):
    print("已讀取Event")
    bot.add_cog(Event(bot))


def teardown(bot):
    print("已移除Event")
    bot.remove_cog("Event")
