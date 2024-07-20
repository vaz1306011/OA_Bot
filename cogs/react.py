import random
import re
from collections import Counter
from functools import partial
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, Modal, TextInput, View

from core.classes import Cog_Extension
from core.logger import logger


class React(Cog_Extension):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @app_commands.command(nsfw=True)
    async def nhentai(self, interaction: discord.Interaction):
        """隨機產生6位數網址

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.defer()
        random_6digit = random.choice(self.DATA["nhentai"])
        await interaction.followup.send(f"https://nhentai.net/g/{random_6digit}")

    @app_commands.command()
    async def say(self, interaction: discord.Interaction, message: str):
        """讓機器人說話

        Args:
            interaction (discord.Interaction): interaction
            message (str): 要讓機器人說的話
        """
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send(message)
        await interaction.followup.send("已發送訊息")

    @app_commands.command()
    async def ranobe(self, interaction: discord.Interaction):
        """拉諾亞魔法大學的圖書館

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.defer()
        embed = discord.Embed(
            title="拉諾亞魔法大學的圖書館",
            url=self.URL["ranobe"],
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    async def vow(
        self,
        interaction: discord.Interaction,
        extra_participants_count: int = 0,
        member1: Optional[discord.Member] = None,
        member2: Optional[discord.Member] = None,
        member3: Optional[discord.Member] = None,
        member4: Optional[discord.Member] = None,
        member5: Optional[discord.Member] = None,
        member6: Optional[discord.Member] = None,
        member7: Optional[discord.Member] = None,
        member8: Optional[discord.Member] = None,
        member9: Optional[discord.Member] = None,
        member10: Optional[discord.Member] = None,
    ):
        """猜拳

        Args:
            interaction (discord.Interaction): interaction
            extra_participants_count (int, optional): 非指定參與者人數
            member1 (Optional[discord.Member], optional): 指定參與者1
            member2 (Optional[discord.Member], optional): 指定參與者2
            member3 (Optional[discord.Member], optional): 指定參與者3
            member4 (Optional[discord.Member], optional): 指定參與者4
            member5 (Optional[discord.Member], optional): 指定參與者5
            member6 (Optional[discord.Member], optional): 指定參與者6
            member7 (Optional[discord.Member], optional): 指定參與者7
            member8 (Optional[discord.Member], optional): 指定參與者8
            member9 (Optional[discord.Member], optional): 指定參與者9
            member10 (Optional[discord.Member], optional): 指定參與者10

        Returns:
            _type_: _description_
        """

        class VOWView(View):
            def __init__(
                self,
                extra_participants_count: int,
                participants: set[discord.Member],
                timeout: Optional[float] = None,
            ) -> None:
                """猜拳按鈕

                Args:
                    extra_participants_count (int): 非指定參與者人數
                    participants (set): 指定參與者清單
                    timeout (float, optional): View持續時間
                """
                super().__init__(timeout=timeout)

                self.extra_participant_count = extra_participants_count
                self.clicked_people = {member.id: None for member in participants}
                self.set_button()

            def set_button(self):
                def check_participant(id: int) -> bool:
                    if id in self.clicked_people.keys():
                        return True

                    if self.extra_participant_count > 0:
                        self.extra_participant_count -= 1
                        return True

                    return False

                async def check_result(interaction: discord.Interaction):
                    logger.info(
                        re.sub(
                            r"\d+",
                            lambda matched: interaction.guild.get_member(
                                int(matched.group())
                            ).nick
                            or interaction.guild.get_member(int(matched.group())).name,
                            str(self.clicked_people),
                        )
                    )

                    if (
                        self.extra_participant_count == 0
                        and None not in self.clicked_people.values()
                    ):
                        await interaction.message.delete()

                        choices = set(self.clicked_people.values())
                        winner = None
                        if len(choices) not in (1, 3):
                            if "✌🏽剪刀" in choices:
                                if "✊🏽石頭" in choices:
                                    winner = "✊🏽石頭"
                                else:
                                    winner = "✌🏽剪刀"

                            else:
                                winner = "✋🏽布"

                        description = ""
                        for user_id, choice in self.clicked_people.items():
                            user = interaction.guild.get_member(user_id)
                            description += f"{user.mention}：{choice}"
                            description += " 👑" if choice == winner else ""
                            description += "\n"

                        embed = discord.Embed(
                            title="猜拳結果", description=description.strip()
                        )
                        await interaction.channel.send(embed=embed)

                V = Button(label="剪刀", emoji="✌🏽")
                O = Button(label="石頭", emoji="✊🏽")
                W = Button(label="布", emoji="✋🏽")

                async def callback(interaction: discord.Interaction, *, choice: str):
                    await interaction.response.defer()
                    if not check_participant(interaction.user.id):
                        return

                    self.clicked_people[interaction.user.id] = choice
                    await check_result(interaction)

                V.callback = partial(callback, choice="✌🏽剪刀")
                O.callback = partial(callback, choice="✊🏽石頭")
                W.callback = partial(callback, choice="✋🏽布")

                for choice in (V, O, W):
                    self.add_item(choice)

        await interaction.response.defer()
        extra_participants_count = max(0, extra_participants_count)
        members = {
            member1,
            member2,
            member3,
            member4,
            member5,
            member6,
            member7,
            member8,
            member9,
            member10,
        }
        members.discard(None)
        members_count = len(members)

        if members_count + extra_participants_count < 2:
            await interaction.followup.send("人數不足", ephemeral=True)
            return

        mentions_string = " ".join((member.mention for member in members))
        extra_participants_count_string = (
            f"你們{extra_participants_count}個"
            if extra_participants_count > 1
            else "你"
        )

        if members_count > 0 and extra_participants_count > 0:
            content = (
                f"{mentions_string}還有{extra_participants_count_string}先別吵過來猜拳"
            )
        elif members_count > 0 and extra_participants_count == 0:
            content = f"{mentions_string}先別吵過來猜拳"
        elif members_count == 0 and extra_participants_count > 0:
            content = f"{extra_participants_count_string}先別吵過來猜拳"

        view = VOWView(extra_participants_count, members)

        await interaction.followup.send(content, view=view)

    @app_commands.command(description="骰骰子")
    async def roll(
        self,
        interaction: discord.Interaction,
        min: int = 1,
        max: int = 20,
    ):
        """骰骰子

        Args:
            interaction (discord.Interaction): interaction
            min (Optional[int], optional): 骰出的最小值(預設為1)
            max (Optional[int], optional): 骰出的最大值(預設為20)
        """
        await interaction.response.defer()
        if min > max:
            await interaction.followup.send("最小值不可大於最大值")
            return

        await interaction.followup.send(
            f"從{min}到{max}骰出 {random.randint(min, max)}"
        )

    @app_commands.command()
    async def vote(
        self,
        interaction: discord.Interaction,
        content: str,
        only_creater_close: bool = True,
        only_creater_add: bool = False,
        only_creater_remove: bool = False,
        only_creater_clean: bool = True,
    ):
        """投票

        Args:
            interaction (discord.Interaction): interaction
            content (str): 投票題目
        """

        class VoteView(discord.ui.View):
            def __init__(self, content, *, timeout: Optional[float] = None):
                super().__init__(timeout=timeout)
                self.author_id = interaction.user.id
                self.content = content
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
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="目前已投票:",
                        description="\n".join(
                            (
                                interaction.guild.get_member(user).mention
                                for user in self.votes.keys()
                            )
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
                if only_creater_close and interaction.user.id != self.author_id:
                    await interaction.followup.send(
                        "只有作者可以關閉投票", ephemeral=True
                    )
                    return

                # 增加0票的選項
                if not self.votes:
                    await interaction.followup.send("還沒有人投票", ephemeral=True)
                    return
                vote_counts = Counter(self.votes.values())
                all_options = [btn.label for btn in self.children[5:]]
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
                    await interaction.followup.send(
                        "你已選擇 " + choice, ephemeral=True
                    )

                new_btn.callback = partial(call_back, choice=option)
                self.add_item(new_btn)

            async def __add_cb(self, interaction: discord.Interaction):
                """新增選項(按鈕callback)

                Args:
                    interaction (discord.Interaction): interaction
                """
                if only_creater_add and interaction.user.id != self.author_id:
                    await interaction.response.defer()
                    await interaction.followup.send(
                        "只有作者可以新增選項", ephemeral=True
                    )
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
                if only_creater_remove and interaction.user.id != self.author_id:
                    await interaction.response.defer()
                    await interaction.followup.send(
                        "只有作者可以刪除選項", ephemeral=True
                    )
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
                    await interaction.followup.send(
                        "請輸入小於選項數量的正整數", ephemeral=True
                    )
                except Exception as e:
                    await interaction.followup.send(e)
                else:
                    if n <= 4 or n >= len(self._children):
                        await interaction.followup.send("超出範圍", ephemeral=True)
                        return

                    removed = self._children.pop(n).label
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

                if only_creater_clean and interaction.user.id != self.author_id:
                    await interaction.followup.send(
                        "只有作者可以清空選項", ephemeral=True
                    )
                    return

                self.votes.clear()
                self._children = self._children[:5]
                await interaction.followup.send("已清空", ephemeral=True)
                await interaction.edit_original_response(view=self)

        embed = discord.Embed(title=content)
        await interaction.response.send_message(embed=embed, view=VoteView(content))


async def setup(bot: commands.Bot):
    await bot.add_cog(React(bot))
    logger.info("已讀取 React 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("React")
    logger.info("已卸載 React 模塊")
