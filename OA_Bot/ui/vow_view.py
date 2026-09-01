import re
from functools import partial
from typing import Optional

import discord
from discord.ui import Button, View

from OA_Bot.core.logger import logger


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
        self.clicked_people: dict[int, Optional[str]] = {
            member.id: None for member in participants
        }
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
            assert interaction.guild is not None
            guild = interaction.guild

            def get_display_name(user_id: int) -> str:
                member = guild.get_member(user_id)
                assert member is not None
                return member.nick or member.name

            logger.info(
                re.sub(
                    r"\d+",
                    lambda matched: get_display_name(int(matched.group())),
                    str(self.clicked_people),
                )
            )

            if (
                self.extra_participant_count == 0
                and None not in self.clicked_people.values()
            ):
                assert interaction.message is not None
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
                    assert user is not None
                    description += f"{user.mention}：{choice}"
                    description += " 👑" if choice == winner else ""
                    description += "\n"

                embed = discord.Embed(title="猜拳結果", description=description.strip())
                assert isinstance(interaction.channel, discord.abc.Messageable)
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
