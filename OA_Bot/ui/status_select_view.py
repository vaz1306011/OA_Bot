from typing import Optional

import discord
from discord import SelectOption
from discord.ext import commands
from discord.ui import Modal, Select, TextInput, View

from OA_Bot.core.data import DataClass
from OA_Bot.core.logger import logger


class QuestionModal(Modal, title="輸入活動名稱"):
    name = TextInput(label="活動名稱")

    def __init__(self, include_url: bool = False):
        super().__init__()
        self.url: Optional[TextInput] = None
        if include_url:
            self.url = TextInput(label="直播網址")
            self.add_item(self.url)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()


class StatusSelectView(View):
    def __init__(self, bot: commands.Bot, data: DataClass):
        super().__init__()
        self.bot = bot
        self.data = data
        self.textInput: Optional[QuestionModal] = None

    @discord.ui.select(
        placeholder="選擇狀態",
        options=[
            SelectOption(label="線上", value="online"),
            SelectOption(label="閒置", value="idle"),
            SelectOption(label="請勿打擾", value="dnd"),
            SelectOption(label="離線", value="offline"),
        ],
    )
    async def status(self, interaction: discord.Interaction, _: Select):
        await interaction.response.defer()

    @discord.ui.select(
        placeholder="選擇活動",
        options=[
            SelectOption(label="無", value="4"),
            SelectOption(label="正在玩", value="0"),
            SelectOption(label="正在直播", value="1"),
            SelectOption(label="正在聽", value="2"),
            SelectOption(label="正在看", value="3"),
            SelectOption(label="競爭", value="5"),
        ],
    )
    async def activity(self, interaction: discord.Interaction, select: Select):
        selected = select.values[0]

        # 沒有活動
        if selected == "4":
            self.textInput = None
            await interaction.response.defer()
            return

        # 活動輸入框
        self.textInput = QuestionModal(include_url=selected == "1")

        # 顯示輸入框
        await interaction.response.send_modal(self.textInput)
        await self.textInput.wait()

    @discord.ui.button(label="確定", style=discord.ButtonStyle.green)
    async def submit(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        type_ = (
            int(self.activity.values[0]) if self.activity.values[0].isdigit() else None
        )

        if type_ != 4 and self.textInput is None:
            await interaction.response.send_message(
                "請先選擇活動並輸入活動名稱", ephemeral=True
            )
            return

        if self.textInput is not None:
            name = self.textInput.name.value
        else:
            name = None

        if self.textInput is not None and self.textInput.url is not None:
            url = self.textInput.url.value
        else:
            url = None

        status = discord.Status(self.status.values[0])
        activity = discord.Activity(type=type_, name=name, url=url)
        await self.bot.change_presence(status=status, activity=activity)
        logger.info(
            f"已設置機器人狀態: {self.status.values[0]} {activity.type=} {activity.name=} {activity.url=}"
        )
        await interaction.response.edit_message(content="設定完成", view=None)
        self.data.presence = {
            "status": status.value,
            "type": type_,
            "name": name,
            "url": url,
        }
        self.data.save()
