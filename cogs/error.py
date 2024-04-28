from discord.ext import commands
from discord.ext.commands import Context

from core.classes import Cog_Extension
from core.logger import logger
from core.tools import ctx_send_red


class Error(Cog_Extension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception):
        from functools import partial

        send = partial(ctx_send_red, ctx)

        if isinstance(error, commands.CommandNotFound):
            await send(f"指令不存在 <{error}>")
        elif isinstance(error, commands.MissingRequiredArgument):
            await send(f"缺少參數 <{error}>")
        elif isinstance(error, commands.BadArgument):
            await send(f"參數錯誤 <{error}>")
        elif isinstance(error, commands.MissingPermissions):
            await send(f"權限不足 <{error}>")
        elif isinstance(error, commands.CommandOnCooldown):
            await send(f"指令過於頻繁 <{error}>")
        elif isinstance(error, commands.CommandInvokeError):
            await send(f"指令執行錯誤 <{error}>")
        elif isinstance(error, commands.CommandError):
            await send(f"指令錯誤 <{error}>")
        else:
            await send(f"發生錯誤 <{error}>")

        """
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

        except commands.CommandOnCooldown as e:
            await send(f"指令過於頻繁 <{e}>")

        except commands.CommandInvokeError as e:
            await send(f"指令執行錯誤 <{e}>")

        except commands.CommandError as e:
            await send(f"指令錯誤 <{e}>")

        except Exception as e:
            await send(f"發生錯誤 <{e}>")
        """


async def setup(bot: commands.Bot):
    await bot.add_cog(Error(bot))
    logger.info("已讀取 Error 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("Error")
    logger.info("已移除 Error 模塊")
