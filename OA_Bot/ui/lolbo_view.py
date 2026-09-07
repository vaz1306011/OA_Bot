import asyncio
import re
from datetime import datetime, timedelta, timezone
from typing import Optional

import discord
from discord import SelectOption
from discord.ui import Button, Modal, Select, TextInput, View

LANES = ["TOP", "JG", "MID", "ADC", "SUP"]
LEAVE_VALUE = "辞退"
FINALIZE_GRACE = timedelta(hours=3)

MODE_LABELS = {
    "flex": "フレックス",
    "duo": "デュオ",
    "aram": "ARAM",
    "normal": "ノーマル",
}

JST = timezone(timedelta(hours=9))


def _parse_clock_time(raw: Optional[str]) -> Optional[datetime]:
    """HH:MM形式の時刻(日本時間)を、直後に訪れるその時刻のdatetimeに変換する。不正な値の場合はNoneを返す"""
    if not raw:
        return None

    match = re.fullmatch(r"([01]?\d|2[0-3]):([0-5]\d)", raw.strip())
    if match is None:
        return None

    hour, minute = int(match.group(1)), int(match.group(2))
    now = datetime.now(JST)
    candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(days=1)
    return candidate


def _format_clock_input(dt: Optional[datetime]) -> Optional[str]:
    """modalの初期値用に、datetimeをHH:MM形式(日本時間)へ変換する"""
    if dt is None:
        return None
    return dt.astimezone(JST).strftime("%H:%M")


def _format_optional_timestamp(dt: Optional[datetime], empty_text: str) -> str:
    if dt is None:
        return empty_text
    timestamp = int(dt.timestamp())
    return f"<t:{timestamp}:f>（<t:{timestamp}:R>）"


class LolboView(View):
    """LOL募集用，顯示各位置狀態並讓其他人選擇要參加的位置"""

    def __init__(
        self,
        author: discord.Member,
        mode: Optional[str],
        lanes: list[str],
        start_time: Optional[datetime] = None,
        deadline: Optional[datetime] = None,
        message_text: Optional[str] = None,
    ):
        super().__init__(timeout=None)
        self.author = author
        self.mode = mode
        self.lanes = lanes
        self.start_time = start_time
        self.deadline = deadline
        self.message_text = message_text
        self.filled: dict[str, int] = {}
        self.closed = False
        self.finalized = False
        self.message: Optional[discord.Message] = None
        self._close_task: Optional[asyncio.Task] = None
        self._finalize_task: Optional[asyncio.Task] = None
        self._build_buttons()
        self._schedule_auto_close()

    def _schedule_auto_close(self):
        if self._close_task is not None:
            self._close_task.cancel()
            self._close_task = None
        if self.deadline is not None and not self.closed:
            self._close_task = asyncio.create_task(self.__auto_close())

    async def __auto_close(self):
        assert self.deadline is not None
        delay = (self.deadline - datetime.now(timezone.utc)).total_seconds()
        if delay > 0:
            await asyncio.sleep(delay)
        if self.closed:
            return
        self.closed = True
        self._build_buttons()
        self._schedule_finalize()
        await self.refresh()

    def _schedule_finalize(self):
        if self._finalize_task is not None:
            self._finalize_task.cancel()
            self._finalize_task = None
        if self.closed and not self.finalized:
            self._finalize_task = asyncio.create_task(self.__finalize())

    async def __finalize(self):
        """募集終了後、一定時間再開されなければボタンを消して終了する"""
        await asyncio.sleep(FINALIZE_GRACE.total_seconds())
        if not self.closed:
            return
        self.finalized = True
        self.clear_items()
        self.stop()
        await self.refresh()

    def _build_buttons(self):
        self.clear_items()
        if self.closed:
            reopen_btn = Button(label="再開", style=discord.ButtonStyle.primary)
            reopen_btn.callback = self.__on_reopen
            self.add_item(reopen_btn)
        else:
            join_btn = Button(label="参加/辞退", style=discord.ButtonStyle.success)
            join_btn.callback = self.__on_participate
            self.add_item(join_btn)

            edit_btn = Button(label="編集", style=discord.ButtonStyle.secondary)
            edit_btn.callback = self.__on_edit
            self.add_item(edit_btn)

            close_btn = Button(label="募集終了", style=discord.ButtonStyle.danger)
            close_btn.callback = self.__on_close
            self.add_item(close_btn)

    def build_embed(self) -> discord.Embed:
        title = f"LOL {MODE_LABELS[self.mode]}募集" if self.mode else "LOL募集"
        if self.closed:
            title += "【募集終了】"
        embed = discord.Embed(title=title)
        embed.add_field(name="発起人", value=self.author.mention, inline=False)
        if self.message_text:
            embed.add_field(name="メッセージ", value=self.message_text, inline=False)
        embed.add_field(
            name="開始時間",
            value=_format_optional_timestamp(self.start_time, "未定"),
            inline=False,
        )
        embed.add_field(
            name="募集期限",
            value=_format_optional_timestamp(self.deadline, "なし"),
            inline=False,
        )
        embed.add_field(
            name="募集人数",
            value=f"{len(self.filled)}/{len(self.lanes)}",
            inline=False,
        )
        lines = [
            f"{lane}　{f'<@{self.filled[lane]}>' if lane in self.filled else '空き'}"
            for lane in self.lanes
        ]
        embed.add_field(name="レーン状況", value="\n".join(lines), inline=False)
        return embed

    async def refresh(self):
        """公開募集訊息重新整理"""
        assert self.message is not None
        await self.message.edit(embed=self.build_embed(), view=self)

    async def __on_participate(self, interaction: discord.Interaction):
        """参加按鈕callback，開啟位置選單

        Args:
            interaction (discord.Interaction): interaction
        """
        if self.closed:
            await interaction.response.send_message(
                "募集は終了しています", ephemeral=True
            )
            return

        join_view = LolboJoinSelectView(self)
        await interaction.response.send_message(
            "レーンを選択してください", view=join_view, ephemeral=True
        )

    async def __on_edit(self, interaction: discord.Interaction):
        """編集按鈕callback

        Args:
            interaction (discord.Interaction): interaction
        """
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "編集できるのは発起人のみです", ephemeral=True
            )
            return

        edit_view = LolboEditView(self)
        await interaction.response.send_message(
            "編集するレーンを選択してください", view=edit_view, ephemeral=True
        )

    async def __on_close(self, interaction: discord.Interaction):
        """募集終了按鈕callback

        Args:
            interaction (discord.Interaction): interaction
        """
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "終了できるのは発起人のみです", ephemeral=True
            )
            return

        self.closed = True
        self._schedule_auto_close()
        self._schedule_finalize()
        self._build_buttons()
        await interaction.response.edit_message(embed=self.build_embed(), view=self)

    async def __on_reopen(self, interaction: discord.Interaction):
        """再開按鈕callback

        Args:
            interaction (discord.Interaction): interaction
        """
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "再開できるのは発起人のみです", ephemeral=True
            )
            return

        self.closed = False
        if self.deadline is not None and self.deadline <= datetime.now(timezone.utc):
            self.deadline = None
        self._build_buttons()
        self._schedule_auto_close()
        self._schedule_finalize()
        await interaction.response.edit_message(embed=self.build_embed(), view=self)


class LolboJoinSelectView(View):
    """LOL募集用，選擇要參加的位置或辭退"""

    def __init__(self, parent: LolboView):
        super().__init__(timeout=60)
        self.parent = parent
        self.select: Select = Select(
            placeholder="レーンを選択",
            options=[
                SelectOption(label=lane)
                for lane in parent.lanes
                if lane not in parent.filled
            ]
            + [SelectOption(label=LEAVE_VALUE, emoji="↩️")],
        )
        self.select.callback = self.__on_select
        self.add_item(self.select)

    async def __on_select(self, interaction: discord.Interaction):
        """位置選單callback

        Args:
            interaction (discord.Interaction): interaction
        """
        choice = self.select.values[0]

        if choice == LEAVE_VALUE:
            joined_lane = next(
                (
                    lane
                    for lane, user_id in self.parent.filled.items()
                    if user_id == interaction.user.id
                ),
                None,
            )
            if joined_lane is None:
                await interaction.response.edit_message(
                    content="参加しているレーンがありません", view=None
                )
                return

            del self.parent.filled[joined_lane]
            await interaction.response.edit_message(content="辞退しました", view=None)
            await self.parent.refresh()
            return

        if choice in self.parent.filled:
            await interaction.response.edit_message(
                content="このレーンは既に選択されています", view=None
            )
            return

        for filled_lane, user_id in list(self.parent.filled.items()):
            if user_id == interaction.user.id:
                del self.parent.filled[filled_lane]

        self.parent.filled[choice] = interaction.user.id
        await interaction.response.edit_message(
            content=f"{choice}に参加しました", view=None
        )
        await self.parent.refresh()


class LolboEditView(View):
    """LOL募集用，讓發起人編輯缺少的位置，接著編輯開始時間、期限與訊息"""

    def __init__(self, parent: LolboView):
        super().__init__(timeout=180)
        self.parent = parent
        self.selected_lane = list(parent.lanes)
        self.select: Select = Select(
            placeholder="募集したいレーンを選択",
            min_values=1,
            max_values=len(LANES),
            options=[
                SelectOption(label=lane, default=lane in parent.lanes) for lane in LANES
            ],
        )
        self.select.callback = self.__on_select_lanes
        self.add_item(self.select)

        confirm_btn = Button(
            label="次へ(時間・メッセージ)", style=discord.ButtonStyle.primary
        )
        confirm_btn.callback = self.__on_confirm
        self.add_item(confirm_btn)

    async def __on_select_lanes(self, interaction: discord.Interaction):
        """位置選單callback

        Args:
            interaction (discord.Interaction): interaction
        """
        self.selected_lane = [lane for lane in LANES if lane in self.select.values]
        await interaction.response.defer()

    async def __on_confirm(self, interaction: discord.Interaction):
        """次へ按鈕callback，開啟時間與訊息編輯用modal

        Args:
            interaction (discord.Interaction): interaction
        """
        modal = LolboEditModal(
            start_time_default=_format_clock_input(self.parent.start_time),
            deadline_default=_format_clock_input(self.parent.deadline),
            message_default=self.parent.message_text,
        )
        await interaction.response.send_modal(modal)
        await modal.wait()

        invalid_fields = []
        if modal.start_time.value and _parse_clock_time(modal.start_time.value) is None:
            invalid_fields.append("開始時間")
        if modal.deadline.value and _parse_clock_time(modal.deadline.value) is None:
            invalid_fields.append("募集期限")

        self.parent.lanes = self.selected_lane
        self.parent.filled = {
            lane: user_id
            for lane, user_id in self.parent.filled.items()
            if lane in self.selected_lane
        }
        self.parent.start_time = _parse_clock_time(modal.start_time.value)
        self.parent.deadline = _parse_clock_time(modal.deadline.value)
        self.parent.message_text = modal.message_text.value or None
        self.parent._build_buttons()
        self.parent._schedule_auto_close()

        if invalid_fields:
            content = f"{'、'.join(invalid_fields)}はHH:MM形式で入力してください。未設定にしました"
        else:
            content = "募集内容を更新しました"
        await interaction.edit_original_response(content=content, view=None)
        await self.parent.refresh()


class LolboEditModal(Modal, title="募集情報を編集"):
    """LOL募集用，編輯開始時間、募集期限與訊息"""

    def __init__(
        self,
        start_time_default: Optional[str],
        deadline_default: Optional[str],
        message_default: Optional[str],
    ):
        super().__init__()
        self.start_time = TextInput(
            label="開始時間 (HH:MM)",
            placeholder="21:30",
            max_length=5,
            required=False,
            default=start_time_default,
        )
        self.deadline = TextInput(
            label="募集期限 (HH:MM)",
            placeholder="23:30",
            max_length=5,
            required=False,
            default=deadline_default,
        )
        self.message_text = TextInput(
            label="メッセージ",
            placeholder="任意",
            max_length=200,
            required=False,
            style=discord.TextStyle.paragraph,
            default=message_default,
        )
        self.add_item(self.start_time)
        self.add_item(self.deadline)
        self.add_item(self.message_text)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()


class LolboLaneSelectView(View):
    """LOL募集初始化用，讓發起人設定時區、模式與缺少的位置"""

    NONE_MODE_VALUE = "none"

    def __init__(self, author: discord.Member):
        super().__init__(timeout=180)
        self.author = author
        self.mode: Optional[str] = None
        self.selected_lanes: list[str] = []

        self.mode_select: Select = Select(
            placeholder="モードを選択",
            options=[
                SelectOption(label=label, value=key)
                for key, label in MODE_LABELS.items()
            ]
            + [SelectOption(label="指定なし", value=self.NONE_MODE_VALUE)],
        )
        self.mode_select.callback = self.__on_select_mode
        self.add_item(self.mode_select)

        self.select: Select = Select(
            placeholder="位置を選択",
            min_values=1,
            max_values=len(LANES),
            options=[SelectOption(label=lane) for lane in LANES],
        )
        self.select.callback = self.__on_select_lanes
        self.add_item(self.select)

        confirm_btn = Button(
            label="次へ(時間・メッセージ)", style=discord.ButtonStyle.primary
        )
        confirm_btn.callback = self.__on_confirm
        self.add_item(confirm_btn)

    async def __on_select_mode(self, interaction: discord.Interaction):
        """モード選單callback

        Args:
            interaction (discord.Interaction): interaction
        """
        selected = self.mode_select.values[0]
        self.mode = None if selected == self.NONE_MODE_VALUE else selected
        await interaction.response.defer()

    async def __on_select_lanes(self, interaction: discord.Interaction):
        """位置選單callback

        Args:
            interaction (discord.Interaction): interaction
        """
        self.selected_lanes = [lane for lane in LANES if lane in self.select.values]
        await interaction.response.defer()

    async def __on_confirm(self, interaction: discord.Interaction):
        """次へ按鈕callback，開啟時間與訊息設定用modal

        Args:
            interaction (discord.Interaction): interaction
        """
        if not self.selected_lanes:
            await interaction.response.send_message(
                "レーンを選択してください", ephemeral=True
            )
            return

        modal = LolboInfoModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        invalid_fields = []
        if modal.start_time.value and _parse_clock_time(modal.start_time.value) is None:
            invalid_fields.append("開始時間")
        if modal.deadline.value and _parse_clock_time(modal.deadline.value) is None:
            invalid_fields.append("募集期限")

        start_time = _parse_clock_time(modal.start_time.value)
        deadline = _parse_clock_time(modal.deadline.value)
        message_text = modal.message_text.value or None

        view = LolboView(
            self.author,
            self.mode,
            self.selected_lanes,
            start_time,
            deadline,
            message_text,
        )
        assert isinstance(interaction.channel, discord.abc.Messageable)
        message = await interaction.channel.send(embed=view.build_embed(), view=view)
        view.message = message

        if invalid_fields:
            await interaction.followup.send(
                f"{'、'.join(invalid_fields)}はHH:MM形式で入力してください。未設定で作成しました",
                ephemeral=True,
            )
        await interaction.delete_original_response()
        self.stop()


class LolboInfoModal(Modal, title="募集情報を設定"):
    """LOL募集初始化用，設定開始時間、募集期限與訊息"""

    start_time = TextInput(
        label="開始時間 (HH:MM)", placeholder="21:30", max_length=5, required=False
    )
    deadline = TextInput(
        label="募集期限 (HH:MM)", placeholder="23:30", max_length=5, required=False
    )
    message_text = TextInput(
        label="メッセージ",
        placeholder="任意",
        max_length=200,
        required=False,
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
