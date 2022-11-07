import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Button, View

from core.classes import Cog_Extension
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
        game = discord.Game(name="吸娜娜奇")
        await self.bot.change_presence(status=discord.Status.idle, activity=game)

    @commands.command()
    async def test3(self, ctx: Context):
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
    async def test4(self, ctx: Context):
        test = self.Role_button(
            role_id=self.role["test"],
            label="test身分組",
            style=discord.ButtonStyle.blurple,
        )

        view = View(timeout=None)
        view.add_item(test)

        await ctx_send(ctx, "加入身分組", view=view)

    test_group = app_commands.Group(name="test", description="測試指令")

    @test_group.command()
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")

    @test_group.command()
    async def test2(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.channel.send("test2")

    @test_group.command()
    async def test3(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send("test1")
        await interaction.followup.send("test2")

    @test_group.command()
    async def test4(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.bot.change_presence(status=discord.Status.online)
        await interaction.followup.send("已更改狀態為: 在線")


async def setup(bot: commands.Bot):
    print("已讀取Test")
    await bot.add_cog(Test(bot))


async def teardown(bot: commands.Bot):
    print("已移除Test")
    await bot.remove_cog("Test")
