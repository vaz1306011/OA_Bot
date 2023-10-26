import random

import discord
from discord import app_commands
from discord.app_commands.errors import AppCommandError
from discord.ext import commands
from discord.ui import Modal, TextInput

from core.classes import Cog_Extension


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
        deleted = await interaction.channel.purge(
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
            answer = TextInput(label="數量", placeholder="1", max_length=2, default=1)

            async def on_submit(self, interaction: discord.Interaction) -> None:
                await interaction.response.defer()

        if message.author.bot:
            await interaction.response.send_message("不能選擇機器人的訊息", ephemeral=True)
            return

        modal = QuestionModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        options = [message.content]
        async for msg in interaction.channel.history(after=message):
            options.append(msg.content)

        if len(options) < int(modal.answer.value):
            await interaction.followup.send("訊息數量不足", ephemeral=True)

        sources_list = "、".join(options)
        selected_items = "、".join(random.sample(options, k=int(modal.answer.value)))
        resault = f"從 {sources_list}\n選出 {selected_items}"
        await interaction.channel.purge(limit=len(options))
        await interaction.followup.send(resault)


async def setup(bot: commands.Bot):
    print("已讀取ContextMenu")
    await bot.add_cog(ContextMenu(bot))


async def teardown(bot: commands.Bot):
    print("已移除ContextMenu")
