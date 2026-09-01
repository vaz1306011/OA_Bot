import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from OA_Bot.core.classes import Cog_Extension
from OA_Bot.core.logger import logger


class Error(Cog_Extension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception):
        pass

    @commands.Cog.listener()
    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CheckFailure):
            return

        message = f"指令執行錯誤 <{error}>"
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Error(bot))
    logger.info("已讀取 Error 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("Error")
    logger.info("已移除 Error 模塊")
