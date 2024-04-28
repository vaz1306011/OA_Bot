import json
from typing import Literal

import discord
from discord import SelectOption, app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Modal, Select, TextInput, View

from bot import CogType
from core.check import is_owner
from core.classes import Cog_Extension
from core.data import DATA
from core.logger import logger
from core.tools import ctx_send


class Main(Cog_Extension):
    @commands.command()
    async def fsync(self, ctx: Context):
        synced = await self.bot.tree.sync()
        await ctx_send(ctx, f"已同步{len(synced)}條指令")

    @app_commands.command(description="載入模塊")
    @app_commands.check(is_owner)
    async def load(self, interaction: discord.Interaction, cog_name: CogType):
        await interaction.response.defer(ephemeral=True)
        cog_name = cog_name.value
        try:
            await self.bot.load_extension(f"cogs.{cog_name}")
            await interaction.followup.send(f"已載入 {cog_name} 模塊")
        except Exception as e:
            await interaction.followup.send(f"載入模塊 {cog_name} 失敗，原因為: {e}")

    @app_commands.command(description="卸載模塊")
    @app_commands.check(is_owner)
    async def unload(self, interaction: discord.Interaction, cog_name: CogType):
        await interaction.response.defer(ephemeral=True)
        cog_name = cog_name.value
        try:
            await self.bot.unload_extension(f"cogs.{cog_name}")
            await interaction.followup.send(f"已卸載 {cog_name} 模塊")
        except Exception as e:
            await interaction.followup.send(f"卸載模塊 {cog_name} 失敗，原因為: {e}")

    @app_commands.command(description="重新載入模塊")
    @app_commands.check(is_owner)
    async def reload(self, interaction: discord.Interaction, cog_name: CogType):
        await interaction.response.defer(ephemeral=True)
        cog_name = cog_name.value
        try:
            if cog_name == "*":
                for cog in CogType:
                    try:
                        await self.bot.unload_extension(f"cogs.{cog.name}")
                        await self.bot.load_extension(f"cogs.{cog.name}")
                    except:
                        pass

                await interaction.followup.send("已重新載入所有Cog")
            else:
                try:
                    await self.bot.unload_extension(f"cogs.{cog_name}")
                except:
                    pass
                finally:
                    await self.bot.load_extension(f"cogs.{cog_name}")

                await interaction.followup.send(f"已重新載入 {cog_name} 模塊")

        except commands.ExtensionNotLoaded as e:
            pass

        except Exception as e:
            await interaction.followup.send(
                f"重新載入模塊 {cog_name} 失敗，原因為: {e}", ephemeral=True
            )

    @app_commands.command(description="同步指令")
    @app_commands.check(is_owner)
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        synced = await self.bot.tree.sync()
        await interaction.followup.send(f"已同步{len(synced)}條指令")

    @app_commands.command(description="設置機器人狀態")
    @app_commands.check(is_owner)
    async def set_status(self, interaction: discord.Interaction):
        class QuestionModal(Modal, title="輸入活動名稱"):
            name = TextInput(label="活動名稱")

            async def on_submit(self, interaction: discord.Interaction) -> None:
                await interaction.response.defer()

        class StatusSelectView(View):
            def __init__(self, bot: commands.Bot):
                super().__init__()
                self.bot = bot
                self.textInput = None
                # self.activity_name = Select(options=[SelectOption(label="無")], row=2)
                # self.add_item(self.activity_name)

            @discord.ui.select(
                placeholder="選擇狀態",
                options=[
                    SelectOption(label="線上", value="online"),
                    SelectOption(label="閒置", value="idle"),
                    SelectOption(label="請勿打擾", value="dnd"),
                    SelectOption(label="離線", value="offline"),
                ],
            )
            async def status(self, interaction: discord.Interaction, select: Select):
                await interaction.response.defer()

            @discord.ui.select(
                placeholder="選擇活動",
                options=[
                    SelectOption(label="無", value="4"),
                    SelectOption(label="正在玩", value="0"),
                    SelectOption(label="正在直播", value="1"),
                    SelectOption(label="正在聽", value="2"),
                    SelectOption(label="正在看", value="3"),
                    SelectOption(label="競爭", value="5"),
                ],
            )
            async def activity(self, interaction: discord.Interaction, select: Select):
                selected = select.values[0]

                # 沒有活動
                if selected == "4":
                    await interaction.response.defer()
                    return

                # 活動輸入框
                self.textInput = QuestionModal()

                # 如果是直播,添加直播網址
                if selected == "1":
                    url = TextInput(label="直播網址")
                    self.textInput.add_item(url)

                # 顯示輸入框
                await interaction.response.send_modal(self.textInput)
                await self.textInput.wait()

                # label = f"{self.textInput.name.value} {self.textInput.children[1].value if len(self.textInput.children) >= 2 else ''}"
                # # print(label)
                # print(self.children[0])
                # self.activity_name._underlying.options[0] = SelectOption(
                #     label=label, default=True
                # )
                # await interaction.edit_original_response(view=self)

            # @discord.ui.select(disabled=True, options=[SelectOption(label="無")])
            # async def activity_name(
            #     self, interaction: discord.Interaction, select: Select
            # ):
            #     await interaction.response.defer()

            @discord.ui.button(label="確定", style=discord.ButtonStyle.green)
            async def submit(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ):
                type_ = (
                    int(self.activity.values[0])
                    if self.activity.values[0].isdigit()
                    else None
                )

                if type_ != 4:
                    name = self.textInput.name.value
                else:
                    name = None

                if type_ == 1:
                    url = self.textInput.children[1].value
                else:
                    url = None

                activity = discord.Activity(type=type_, name=name, url=url)
                await self.bot.change_presence(
                    status=self.status.values[0], activity=activity
                )
                logger.info(
                    f"已設置機器人狀態: {self.status.values[0]} {activity.type=} {activity.name=} {activity.url=}"
                )
                await interaction.response.edit_message(content="設定完成", view=None)
                DATA["presence"] = {
                    "status": self.status.values[0],
                    "type": type_,
                    "name": name,
                    "url": url,
                }
                json.dump(
                    DATA,
                    open(
                        "./data/data.json",
                        "w",
                        encoding="utf8",
                    ),
                    indent=2,
                    ensure_ascii=False,
                )

        view = StatusSelectView(self.bot)
        await interaction.response.send_message(view=view, ephemeral=True)

    @app_commands.command(description="顯示ping值")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{round(self.bot.latency*1000)}毫秒", ephemeral=True
        )

    @app_commands.command(description="顯示幫助訊息")
    async def help(
        self, interaction: discord.Interaction, cog_name: Literal["id", "omi"] = None
    ):
        embed = discord.Embed(title="普通使用者可以用的指令")
        embed.set_author(
            name="OA_Bot",
            icon_url="https://cdn.discordapp.com/app-icons/799467265010565120/0fa1c461084546f2f69fca5a05046de3.png?size=512&quot",
        )
        match cog_name:
            case None:
                embed.add_field(name="/ping", value="顯示ping值", inline=True)
                embed.add_field(name="/vow", value="猜拳", inline=True)
                embed.add_field(name="/vote", value="投票", inline=True)
                embed.add_field(name="/roll", value="骰骰子", inline=True)
                embed.add_field(name="/say", value="讓機器人說話", inline=True)
                embed.add_field(name="/nhentai", value="隨機產生6位數網址", inline=True)
                embed.add_field(name="/novel", value="獲取小說雲端網址", inline=True)

            case "id":
                embed.add_field(name="/id member", value="查詢成員id", inline=True)
                embed.add_field(name="/id role", value="查詢身分組id", inline=True)
                embed.add_field(name="/id channel", value="查詢頻道id", inline=True)
                embed.add_field(name="/id guild", value="查詢伺服器id", inline=True)

            case "omi":
                embed.add_field(
                    name="/omi guild", value="忽略伺服器的關鍵字檢測", inline=True
                )
                embed.add_field(
                    name="/omi channel", value="忽略頻道的關鍵字檢測", inline=True
                )
                embed.add_field(name="/omi me", value="忽略你的關鍵字檢測", inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
    logger.info("已讀取 Main 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("Main")
    logger.info("已移除 Main 模塊")
