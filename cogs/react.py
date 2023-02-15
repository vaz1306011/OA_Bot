import random
import re
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, View

from core.check import is_owner
from core.classes import Cog_Extension


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
        await interaction.response.defer()
        await interaction.followup.send("已發送訊息", ephemeral=True)
        await interaction.channel.send(message)

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
                    n (int): 非指定參與者人數
                    participant (set): 指定參與者清單
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

                async def V_cb(interaction: discord.Interaction):
                    await interaction.response.defer()
                    if not check_participant(interaction.user.id):
                        return

                    self.clicked_people[interaction.user.id] = "✌🏽剪刀"
                    await check_result(interaction)

                async def O_cb(interaction: discord.Interaction):
                    await interaction.response.defer()
                    if not check_participant(interaction.user.id):
                        return

                    self.clicked_people[interaction.user.id] = "✊🏽石頭"
                    await check_result(interaction)

                async def W_cb(interaction: discord.Interaction):
                    await interaction.response.defer()
                    if not check_participant(interaction.user.id):
                        return

                    self.clicked_people[interaction.user.id] = "✋🏽布"
                    await check_result(interaction)

                V = Button(label="剪刀", emoji="✌🏽")
                O = Button(label="石頭", emoji="✊🏽")
                W = Button(label="布", emoji="✋🏽")

                V.callback = V_cb
                O.callback = O_cb
                W.callback = W_cb

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

    @app_commands.command(description="隨機選擇器")
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

        await interaction.followup.send("\n".join(random.sample(msgs, k=m)))
        await interaction.channel.purge(limit=len(msgs), before=interaction.created_at)


async def setup(bot: commands.Bot):
    print("已讀取React")
    await bot.add_cog(React(bot))


async def teardown(bot: commands.Bot):
    print("已移除React")
    await bot.remove_cog("React")
