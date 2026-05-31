import random

import discord
from discord import app_commands
from discord.app_commands.errors import AppCommandError
from discord.ext import commands
from discord.ui import Modal, TextInput

from OA_Bot.core.classes import Cog_Extension
from OA_Bot.core.logger import logger


class ContextMenu(Cog_Extension):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        clear_after_error = discord.app_commands.ContextMenu(
            name="清理之後的訊息", callback=self.clear_after
        )
        clear_after_error.error(self.clear_after_error)
        self.bot.tree.add_command(clear_after_error)

        choose = discord.app_commands.ContextMenu(name="隨機選擇", callback=self.choose)
        # choose.error(self.choose_error)
        self.bot.tree.add_command(choose)

    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_after(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        """清理之後的訊息

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.defer(ephemeral=True)
        channel = message.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.followup.send("此功能只能在伺服器文字頻道中使用")
            return

        deleted = await channel.purge(
            limit=None, check=lambda msg: msg.id >= message.id
        )
        await interaction.followup.send(f"已刪除{len(deleted)}則訊息")

    async def clear_after_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("你沒有權限", ephemeral=True)

    async def choose(self, interaction: discord.Interaction, message: discord.Message):
        """隨機選擇器

        Args:
            interaction (discord.Interaction): interaction
            message (discord.Message): 訊息
        """

        class QuestionModal(Modal, title="選出幾個"):
            answer = TextInput(label="數量", placeholder="1", max_length=2, default="1")

            async def on_submit(self, interaction: discord.Interaction) -> None:
                await interaction.response.defer()

        if message.author.bot:
            await interaction.response.send_message(
                "不能選擇機器人的訊息", ephemeral=True
            )
            return

        modal = QuestionModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        channel = message.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.followup.send(
                "此功能只能在伺服器文字頻道中使用", ephemeral=True
            )
            return

        try:
            count = int(modal.answer.value)
        except ValueError:
            await interaction.followup.send("請輸入有效的數量", ephemeral=True)
            return

        if count < 1:
            await interaction.followup.send("數量必須大於 0", ephemeral=True)
            return

        options = [message.content]
        async for msg in channel.history(after=message):
            options.append(msg.content)

        if len(options) < count:
            await interaction.followup.send("訊息數量不足", ephemeral=True)
            return

        sources_list = "、".join(options)
        selected_items = "、".join(random.sample(options, k=count))
        resault = f"從 {sources_list}\n選出 {selected_items}"
        await channel.purge(limit=len(options))
        await interaction.followup.send(resault)


async def setup(bot: commands.Bot):
    await bot.add_cog(ContextMenu(bot))
    logger.info("已讀取 ContextMenu 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("ContextMenu")
    logger.info("已移除 ContextMenu 模塊")
