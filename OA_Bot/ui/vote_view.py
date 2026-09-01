from collections import Counter
from functools import partial
from typing import Optional

import discord
from discord.ui import Button, Modal, TextInput, View


class VoteView(View):
    def __init__(
        self,
        author_id: int,
        content: str,
        only_creater_close: bool = True,
        only_creater_add: bool = False,
        only_creater_remove: bool = False,
        only_creater_clean: bool = True,
        *,
        timeout: Optional[float] = None,
    ):
        super().__init__(timeout=timeout)
        self.author_id = author_id
        self.content = content
        self.only_creater_close = only_creater_close
        self.only_creater_add = only_creater_add
        self.only_creater_remove = only_creater_remove
        self.only_creater_clean = only_creater_clean
        self.votes = dict()
        self.init_button()

    def init_button(self):
        self.clear_items()
        check_vote_btn = Button(emoji="📋", style=discord.ButtonStyle.success)
        close_btn = Button(emoji="✔️", style=discord.ButtonStyle.blurple)
        add_btn = Button(emoji="➕", style=discord.ButtonStyle.success)
        remove_btn = Button(emoji="➖", style=discord.ButtonStyle.red)
        clean_btn = Button(label="C", style=discord.ButtonStyle.gray)

        check_vote_btn.callback = self.__check_votes_cb
        close_btn.callback = self.__close_cb
        add_btn.callback = self.__add_cb
        remove_btn.callback = self.__remove_cb
        clean_btn.callback = self.__clean_cb

        for btn in (
            check_vote_btn,
            close_btn,
            add_btn,
            remove_btn,
            clean_btn,
        ):
            self.add_item(btn)

    async def __check_votes_cb(self, interaction: discord.Interaction):
        """檢查誰有投票(按鈕callback)

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.defer()
        assert interaction.guild is not None
        guild = interaction.guild

        def get_mention(user_id: int) -> str:
            member = guild.get_member(user_id)
            assert member is not None
            return member.mention

        await interaction.followup.send(
            embed=discord.Embed(
                title="目前已投票:",
                description="\n".join(
                    (get_mention(user) for user in self.votes.keys())
                ),
            ),
            ephemeral=True,
        )

    async def __close_cb(self, interaction: discord.Interaction):
        """關閉投票(按鈕callback)

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.defer()

        # 別人不能投票
        if self.only_creater_close and interaction.user.id != self.author_id:
            await interaction.followup.send("只有作者可以關閉投票", ephemeral=True)
            return

        # 增加0票的選項
        if not self.votes:
            await interaction.followup.send("還沒有人投票", ephemeral=True)
            return
        vote_counts = Counter(self.votes.values())
        all_options: list[str] = []
        for btn in self.children[5:]:
            assert isinstance(btn, Button) and btn.label is not None
            all_options.append(btn.label)
        for option in all_options:
            vote_counts.setdefault(option, 0)

        # 計算結果
        most_common_options = []
        other_options = []
        for option, vcount in vote_counts.most_common():
            if vcount == vote_counts.most_common(1)[0][1]:
                most_common_options.append(f"{vcount}票{option}")
            else:
                other_options.append(f"{vcount}票{option}")

        description = f"結果: "
        description += "、".join(most_common_options) + "👑"
        if other_options:
            description += f"\n其他: {'、'.join(other_options)}"

        embed = discord.Embed(title=self.content, description=description)
        await interaction.edit_original_response(embed=embed, view=None)

    def _add_option(self, option: str):
        """新增選項

        Args:
            option (str): 選項文字
        """
        new_btn = Button(label=option, style=discord.ButtonStyle.blurple)

        async def call_back(interaction: discord.Interaction, *, choice: str):
            await interaction.response.defer()
            self.votes[interaction.user.id] = choice
            await interaction.followup.send("你已選擇 " + choice, ephemeral=True)

        new_btn.callback = partial(call_back, choice=option)
        self.add_item(new_btn)

    async def __add_cb(self, interaction: discord.Interaction):
        """新增選項(按鈕callback)

        Args:
            interaction (discord.Interaction): interaction
        """
        if self.only_creater_add and interaction.user.id != self.author_id:
            await interaction.response.defer()
            await interaction.followup.send("只有作者可以新增選項", ephemeral=True)
            return

        class QuestionModal(Modal, title="新增選項"):
            answer = TextInput(label="選項", placeholder="選項", max_length=80)

            async def on_submit(self, interaction: discord.Interaction) -> None:
                await interaction.response.defer()

        modal = QuestionModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        self._add_option(modal.answer.value)
        await interaction.edit_original_response(view=self)

    async def __remove_cb(self, interaction: discord.Interaction):
        """刪除選項(按鈕callback)

        Args:
            interaction (discord.Interaction): interaction
        """
        if self.only_creater_remove and interaction.user.id != self.author_id:
            await interaction.response.defer()
            await interaction.followup.send("只有作者可以刪除選項", ephemeral=True)
            return

        class QuestionModal(Modal, title="刪除選項"):
            answer = TextInput(label="index", placeholder="index", max_length=2)

            async def on_submit(self, interaction: discord.Interaction) -> None:
                await interaction.response.defer()

        modal = QuestionModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            n = int(modal.answer.value) - 1 + 5
        except ValueError:
            await interaction.followup.send("請輸入小於選項數量的正整數", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(str(e))
        else:
            if n <= 4 or n >= len(self._children):
                await interaction.followup.send("超出範圍", ephemeral=True)
                return

            removed_item = self._children.pop(n)
            assert isinstance(removed_item, Button) and removed_item.label is not None
            removed = removed_item.label
            self.votes = {
                user: choice
                for user, choice in self.votes.items()
                if choice != removed
            }
            await interaction.followup.send(f"已刪除 {removed}", ephemeral=True)
            await interaction.edit_original_response(view=self)

    async def __clean_cb(self, interaction: discord.Interaction):
        """清除所有選項(按鈕callback)

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.defer()

        if self.only_creater_clean and interaction.user.id != self.author_id:
            await interaction.followup.send("只有作者可以清空選項", ephemeral=True)
            return

        self.votes.clear()
        self._children = self._children[:5]
        await interaction.followup.send("已清空", ephemeral=True)
        await interaction.edit_original_response(view=self)
