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
from core.tools import ctx_send


class Test(Cog_Extension):
    @commands.command()
    async def test(self, ctx: Context):
        await ctx_send(ctx, "red", color="r")
        await ctx_send(ctx, "orange", color="o")
        await ctx_send(ctx, "yellow", color="y")
        await ctx_send(ctx, "green", color="g")
        await ctx_send(ctx, "lightGreen", color="lg")
        await ctx_send(ctx, "blue", color="b")

    @commands.command()
    async def test2(self, ctx: Context):
        btn1 = Button(
            label="白媽媽",
            style=discord.ButtonStyle.blurple,
            emoji="🥵",
        )
        btn2 = Button(
            label="藍媽媽",
            style=discord.ButtonStyle.blurple,
            emoji="🥵",
        )
        btn3 = Button(
            label="紅媽媽",
            style=discord.ButtonStyle.blurple,
            emoji="🥵",
        )

        async def btn1_callback(interaction: discord.Interaction):
            await interaction.response.defer()
            await interaction.channel.send(f"{interaction.user.mention} 先不要白媽媽")

        async def btn2_callback(interaction: discord.Interaction):
            await interaction.response.defer()
            await interaction.channel.send(f"{interaction.user.mention} 先不要藍媽媽")

        async def btn3_callback(interaction: discord.Interaction):
            await interaction.response.defer()
            await interaction.channel.send(f"{interaction.user.mention} 先不要紅媽媽")

        btn1.callback = btn1_callback
        btn2.callback = btn2_callback
        btn3.callback = btn3_callback

        view = View(timeout=None)
        view.add_item(btn1)
        view.add_item(btn2)
        view.add_item(btn3)

        await ctx_send(ctx, "再點直接羈押", view=view)

    @commands.command()
    async def test3(self, ctx: Context):
        class RoleButton(Button):
            def __init__(
                self,
                role_id,
                label: str,
                style: discord.ButtonStyle,
                emoji: str,
                **kwargs,
            ) -> None:
                super().__init__(label=label, style=style, emoji=emoji, **kwargs)
                self.role_id = role_id

            async def callback(self, interaction: discord.Interaction) -> None:
                await interaction.response.defer()
                role = interaction.guild.get_role(self.role_id)
                if role is None:
                    await interaction.channel.send("找不到身分組")

                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
                    await interaction.channel.send(
                        f"已將{interaction.user.mention} 移除 {role.mention}"
                    )

                else:
                    await interaction.user.add_roles(role)
                    await interaction.channel.send(
                        f"已將{interaction.user.mention} 加入 {role.mention}"
                    )

        test = RoleButton(
            role_id=self.ROLE["test"],
            label="test身分組",
            style=discord.ButtonStyle.blurple,
        )

        view = View(timeout=None)
        view.add_item(test)

        await ctx_send(ctx, "加入身分組", view=view)

    test_group = app_commands.Group(name="test", description="test指令群組")

    @test_group.command()
    @app_commands.check(is_owner)
    async def permissions(self, interaction: discord.Interaction, test: str):
        await interaction.response.send_message(f"你有管理員權限 {test}")

    @test_group.command()
    @app_commands.check(is_owner)
    async def test4(self, interaction: discord.Interaction):
        await interaction.response.defer()

    @test_group.command()
    async def test5(self, interaction: discord.Interaction, content: str):
        class MyView(discord.ui.View):
            def __init__(self, *, timeout: Optional[float] = None):
                super().__init__(timeout=timeout)
                self.voted = dict()

                add_btn = Button(
                    label="+",
                    style=discord.ButtonStyle.success,
                )
                add_btn.callback = self.create_cb
                self.add_item(add_btn)

                add_btn = Button(label="-", style=discord.ButtonStyle.red)
                add_btn.callback = self.destroy_cb
                self.add_item(add_btn)

                add_btn = Button(label="c", style=discord.ButtonStyle.blurple)
                add_btn.callback = self.clean_cb
                self.add_item(add_btn)

                add_btn = Button(
                    label="=",
                    style=discord.ButtonStyle.gray,
                )
                add_btn.callback = self.end_cb
                self.add_item(add_btn)

                add_btn = Button(
                    label="test",
                    style=discord.ButtonStyle.success,
                    disabled=True,
                )
                self.add_item(add_btn)

            async def create_cb(self, interaction: discord.Interaction):
                class QuestionModal(Modal, title="新增選項"):
                    answer = TextInput(label="新增的選項", placeholder="選項", max_length=80)

                    async def on_submit(
                        _self, _interaction: discord.Interaction
                    ) -> None:
                        await _interaction.response.defer()
                        self.create_button(_self.answer.value)
                        await interaction.edit_original_response(view=self)

                await interaction.response.send_modal(QuestionModal())

            async def destroy_cb(self, interaction: discord.Interaction):
                await interaction.response.defer()

            async def clean_cb(self, interaction: discord.Interaction):
                self._children = self._children[:5]
                await interaction.response.edit_message(view=self)

            async def end_cb(self, interaction: discord.Interaction):
                await interaction.response.defer()

            def create_button(self, label: str):
                async def call_back(interaction: discord.Interaction, *, label):
                    await interaction.response.defer()

                new_btn = Button(label=label, style=discord.ButtonStyle.blurple)
                new_btn.callback = partial(call_back, label=label)
                self.add_item(new_btn)

        await interaction.response.send_message(content, view=MyView())


async def setup(bot: commands.Bot):
    print("已讀取Test")
    await bot.add_cog(Test(bot), guild=discord.Object(GUILD["老屁股"]))


async def teardown(bot: commands.Bot):
    print("已移除Test")
    await bot.remove_cog("Test")
