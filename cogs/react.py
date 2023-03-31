import random
import re
from collections import Counter
from functools import partial
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, Modal, TextInput, View

from core.check import is_owner
from core.classes import Cog_Extension
from core.data import GUILD


class React(Cog_Extension):
    @commands.command()
    @commands.check(is_owner)
    async def cls(self, ctx: Context, num: int = 0):
        """清理訊息

        Args:
            ctx (Context): ctx
            num (int, optional): 要刪除的訊息數量
        """
        if ctx.message.reference is not None:
            msg_id = ctx.message.reference.message_id
            num = 0
            async for msg in ctx.channel.history():
                if msg.id == msg_id:
                    break
                num += 1

        if num <= 0:
            return

        await ctx.channel.purge(limit=max(0, num) + 1)

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
    async def novel(self, interaction: discord.Interaction):
        """獲取小說雲端網址

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.defer()
        embed = discord.Embed(
            title="小說雲端網址",
            url=self.URL["novel"],
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
                    print(
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

                async def callback(interaction: discord.Interaction, *, choice: str):
                    await interaction.response.defer()
                    if not check_participant(interaction.user.id):
                        return

                    self.clicked_people[interaction.user.id] = choice
                    await check_result(interaction)

                V = Button(label="剪刀", emoji="✌🏽")
                O = Button(label="石頭", emoji="✊🏽")
                W = Button(label="布", emoji="✋🏽")

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
            await interaction.followup.send("人數不足")
            return

        mentions_string = " ".join((member.mention for member in members))
        extra_participants_count_string = (
            f"你們{extra_participants_count}個" if extra_participants_count > 1 else "你"
        )

        if members_count > 0 and extra_participants_count > 0:
            content = f"{mentions_string}還有{extra_participants_count_string}先別吵過來猜拳"
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

        await interaction.followup.send(f"從{min}到{max}骰出 {random.randint(min, max)}")

    @app_commands.command()
    async def choose(self, interaction: discord.Interaction, n: int, m: int = 1):
        """隨機選擇器

        Args:
            interaction (discord.Interaction): interaction
            n (int): 從上n條訊息中選擇(最多20)
            m (int): 選擇m條訊息
        """
        await interaction.response.defer()
        msgs = []
        async for message in interaction.channel.history(
            limit=min(n, 20), before=interaction.created_at
        ):
            if message.author.bot:
                break
            msgs.append(message.content)

        sources_list = "、".join(msgs)
        selected_items = "、".join(random.sample(msgs, k=m))
        resault = f"從 {sources_list}\n選出 " + selected_items

        await interaction.followup.send(resault)
        await interaction.channel.purge(limit=len(msgs), before=interaction.created_at)

    @app_commands.command()
    async def vote(self, interaction: discord.Interaction, content: str):
        class VoteView(discord.ui.View):
            def __init__(self, content, *, timeout: Optional[float] = None):
                super().__init__(timeout=timeout)
                self.content = content
                self.votes = dict()
                self.init_button()

            def init_button(self):
                self.clear_items()
                highest_vote = Button(
                    label="test", style=discord.ButtonStyle.success, disabled=True
                )
                close_btn = Button(emoji="✔️", style=discord.ButtonStyle.blurple)
                create_btn = Button(emoji="➕", style=discord.ButtonStyle.success)
                destroy_btn = Button(emoji="➖", style=discord.ButtonStyle.red)
                clean_btn = Button(label="C", style=discord.ButtonStyle.gray)

                close_btn.callback = self.__close_cb
                create_btn.callback = self.__create_cb
                destroy_btn.callback = self.__remove_cb
                clean_btn.callback = self.__clean_cb

                for btn in (
                    highest_vote,
                    close_btn,
                    create_btn,
                    destroy_btn,
                    clean_btn,
                ):
                    self.add_item(btn)

            def add_option(self, option: str):
                new_btn = Button(label=option, style=discord.ButtonStyle.blurple)

                async def call_back(interaction: discord.Interaction, *, choice: str):
                    await interaction.response.defer()
                    if interaction.user.id not in self.votes:
                        await interaction.followup.send(
                            f"{interaction.user.mention}已投票"
                        )
                    self.votes[interaction.user.id] = choice
                    await interaction.followup.send("你已選擇 " + choice, ephemeral=True)

                new_btn.callback = partial(call_back, choice=option)
                self.add_item(new_btn)

            async def __create_cb(self, interaction: discord.Interaction):
                class QuestionModal(Modal, title="新增選項"):
                    answer = TextInput(label="選項", placeholder="選項", max_length=80)

                    async def on_submit(self, interaction: discord.Interaction) -> None:
                        await interaction.response.defer()

                modal = QuestionModal()
                await interaction.response.send_modal(modal)
                await modal.wait()
                self.add_option(modal.answer.value)
                await interaction.edit_original_response(view=self)

            async def __remove_cb(self, interaction: discord.Interaction):
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
                    await interaction.followup.send(e)
                else:
                    if n <= 4 or n >= len(self._children):
                        await interaction.followup.send("超出範圍", ephemeral=True)
                        return

                    removed = self._children.pop(n).label
                    await interaction.followup.send(f"已刪除 {removed}", ephemeral=True)
                    await interaction.edit_original_response(view=self)

            async def __clean_cb(self, interaction: discord.Interaction):
                await interaction.response.defer()
                self.votes.clear()
                self._children = self._children[:5]
                await interaction.followup.send("已清空", ephemeral=True)
                await interaction.edit_original_response(view=self)

            async def __close_cb(self, interaction: discord.Interaction):
                await interaction.response.defer()
                if not self.votes:
                    await interaction.followup.send("還沒有人投票", ephemeral=True)
                    return
                vote_counts = Counter(self.votes.values())
                all_options = [btn.label for btn in self.children[5:]]
                for option in all_options:
                    vote_counts.setdefault(option, 0)
                most_common_options = []
                other_options = []
                for option, vcount in vote_counts.most_common():
                    if vcount == vote_counts.most_common(1)[0][1]:
                        most_common_options.append(f"{vcount}票{option}")
                    else:
                        other_options.append(f"{vcount}票{option}")

                content = f"{self.content}\n結果: "
                content += "、".join(most_common_options) + "👑"
                if other_options:
                    content += f"\n其他: {'、'.join(other_options)}"

                await interaction.edit_original_response(content=content, view=None)

        await interaction.response.send_message(content, view=VoteView(content))


async def setup(bot: commands.Bot):
    print("已讀取React")
    await bot.add_cog(React(bot))


async def teardown(bot: commands.Bot):
    print("已移除React")
    await bot.remove_cog("React")
