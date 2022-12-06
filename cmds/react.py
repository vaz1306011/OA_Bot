import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, View

from core.check import is_owner_ctx
from core.classes import Cog_Extension


class React(Cog_Extension):
    @commands.command(brief="清理訊息")
    @is_owner_ctx()
    async def cls(self, ctx: Context, num: int = 0):
        if ctx.message.reference is not None:
            msg_id = ctx.message.reference.message_id
            num = 0
            async for msg in ctx.channel.history():
                if msg.id == msg_id:
                    break
                num += 1

        await ctx.channel.purge(limit=max(0, num) + 1)

    @app_commands.command(description="隨機產生6位數網址")
    async def nhentai(self, interaction: discord.Interaction):
        random_6digit = random.choice(self.data["nhentai"])
        await interaction.response.send_message(
            f"https://nhentai.net/g/{random_6digit}"
        )

    @app_commands.command(description="讓機器人說話")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message("已發送訊息", ephemeral=True)
        await interaction.channel.send(message)

    @app_commands.command(description="顯示小說下載雲端連結")
    async def novel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="小說雲端網址",
            url=self.URL["novel"],
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="猜拳")
    async def vow(
        self,
        interaction: discord.Interaction,
        number_of_people: int = None,
        member1: discord.Member | None = None,
        member2: discord.Member | None = None,
        member3: discord.Member | None = None,
        member4: discord.Member | None = None,
        member5: discord.Member | None = None,
        member6: discord.Member | None = None,
        member7: discord.Member | None = None,
        member8: discord.Member | None = None,
        member9: discord.Member | None = None,
        member10: discord.Member | None = None,
    ):
        class VOWView(View):
            def __init__(
                self,
                n: int | None = 0,
                participant: set | None = None,
                timeout: float | None = None,
            ) -> None:
                """猜拳按鈕

                Args:
                    n (int | None, optional): 人數. Defaults to None.
                    participant (list | None, optional): 參與者清單. Defaults to None.
                    timeout (float, optional): View持續時間. Defaults to None.
                """
                if participant is None:
                    participant = set()

                n = max(n, len(participant))

                super().__init__(timeout=timeout)
                if n < 2:
                    raise commands.BadArgument("人數不足")

                self.n = n
                self.participant = participant
                self.clicked_people = dict()
                self.set_button()

            def set_button(self):
                def check_id(id: int) -> bool:
                    if self.participant:
                        if id not in self.participant:
                            return False

                    return True

                async def check_end(interaction: discord.Interaction):
                    print(self.clicked_people)
                    if len(self.clicked_people) >= self.n:
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
                    if not check_id(interaction.user.id):
                        return

                    self.clicked_people[interaction.user.id] = "✌🏽剪刀"
                    await check_end(interaction)

                async def O_cb(interaction: discord.Interaction):
                    await interaction.response.defer()
                    if not check_id(interaction.user.id):
                        return

                    self.clicked_people[interaction.user.id] = "✊🏽石頭"
                    await check_end(interaction)

                async def W_cb(interaction: discord.Interaction):
                    await interaction.response.defer()
                    if not check_id(interaction.user.id):
                        return

                    self.clicked_people[interaction.user.id] = "✋🏽布"
                    await check_end(interaction)

                V = Button(label="剪刀", emoji="✌🏽")
                O = Button(label="石頭", emoji="✊🏽")
                W = Button(label="布", emoji="✋🏽")

                V.callback = V_cb
                O.callback = O_cb
                W.callback = W_cb

                for choice in (V, O, W):
                    self.add_item(choice)

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
        if number_of_people is not None:
            if number_of_people >= 2:
                view = VOWView(n=number_of_people)
                await interaction.response.send_message(
                    f"你們{number_of_people}個先別吵過來猜拳", view=view
                )
            else:
                raise commands.BadArgument("請輸入大於2的正整數")
        else:
            mentions = " ".join(
                (member.mention for member in members if member is not None)
            )
            participant = {member.id for member in members}
            view = VOWView(participant=participant)
            await interaction.response.send_message(f"{mentions}先別吵過來猜拳", view=view)

    @app_commands.command(description="骰骰子")
    async def roll(
        self,
        interaction: discord.Interaction,
        n: int | None = None,
        m: int | None = None,
    ):
        match n, m:
            case None, None:
                n, m = 1, 20

            case n, None:
                n, m = min(1, n), max(1, n)

            case n, m:
                n, m = min(n, m), max(n, m)

        await interaction.response.send_message(f"從{n}到{m}骰出 {random.randint(n, m)}")

    @app_commands.command(description="隨機選擇器")
    async def choose(self, interaction: discord.Interaction, num: int):
        await interaction.response.defer()
        msgs = [
            msg.content
            async for msg in interaction.channel.history(
                limit=num, before=interaction.created_at
            )
        ]
        await interaction.followup.send(random.choice(msgs))
        await interaction.channel.purge(limit=num, before=interaction.created_at)

    @app_commands.command(description="AI作畫")
    async def draw(self, interaction: discord.Interaction, text: str, n: int = 1):
        await interaction.response.defer()
        import os

        import openai

        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.Image.create(prompt=text, n=n, size="1024x1024")
        for url in response["data"]:
            await interaction.followup.send(url["url"])


async def setup(bot: commands.Bot):
    print("已讀取React")
    await bot.add_cog(React(bot))


async def teardown(bot: commands.Bot):
    print("已移除React")
    await bot.remove_cog("React")
