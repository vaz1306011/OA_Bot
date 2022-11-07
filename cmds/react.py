import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

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
                view = self.VOWView(n=number_of_people)
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
            view = self.VOWView(participant=participant)
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


async def setup(bot: commands.Bot):
    print("已讀取React")
    await bot.add_cog(React(bot))


async def teardown(bot: commands.Bot):
    print("已移除React")
    await bot.remove_cog("React")
