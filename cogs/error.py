from discord.ext import commands
from discord.ext.commands import Context

from core.classes import Cog_Extension
from core.tools import ctx_send_red


class Error(Cog_Extension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception):
        from functools import partial

        def send():
            ...

        send = partial(ctx_send_red, ctx)

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


async def setup(bot: commands.Bot):
    print("已讀取Error")
    await bot.add_cog(Error(bot))


async def teardown(bot: commands.Bot):
    print("已移除Error")
    await bot.remove_cog("Error")
