import random
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from OA_Bot.core.classes import Cog_Extension
from OA_Bot.core.logger import logger
from OA_Bot.ui.vote_view import VoteView
from OA_Bot.ui.vow_view import VOWView


class React(Cog_Extension):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @app_commands.command()
    async def say(self, interaction: discord.Interaction, message: str):
        """讓機器人說話

        Args:
            interaction (discord.Interaction): interaction
            message (str): 要讓機器人說的話
        """
        await interaction.response.defer(ephemeral=True)
        assert isinstance(interaction.channel, discord.abc.Messageable)
        await interaction.channel.send(message)
        await interaction.followup.send("已發送訊息")

    @app_commands.command()
    async def ranobe(self, interaction: discord.Interaction):
        """拉諾亞魔法大學的圖書館

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.defer()

        try:
            url = self.data.url["ranobe"]
        except (KeyError, TypeError):
            await interaction.followup.send("拉諾亞魔法大學的圖書館休館中")
            return

        embed = discord.Embed(
            title="拉諾亞魔法大學的圖書館",
            url=url,
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    async def syukudai(self, interaction: discord.Interaction):
        """宿題

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.defer()

        try:
            url = self.data.url["syukudai"]
        except (KeyError, TypeError):
            await interaction.followup.send("ロキシー先生今宿題がありません。")
            return

        embed = discord.Embed(title="ロキシー先生の宿題", url=url)
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

        await interaction.response.defer()
        extra_participants_count = max(0, extra_participants_count)
        members: set[discord.Member] = {
            member
            for member in (
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
            )
            if member is not None
        }
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
        else:
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

        embed = discord.Embed(title=content)
        view = VoteView(
            interaction.user.id,
            content,
            only_creater_close,
            only_creater_add,
            only_creater_remove,
            only_creater_clean,
        )
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(React(bot))
    logger.info("已讀取 React 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("React")
    logger.info("已卸載 React 模塊")
