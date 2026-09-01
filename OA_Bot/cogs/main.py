from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from OA_Bot.bot import COG_CHOICES
from OA_Bot.core.check import is_owner
from OA_Bot.core.classes import Cog_Extension
from OA_Bot.core.consts import TEST_GUILDS, test_only
from OA_Bot.core.logger import logger
from OA_Bot.core.tools import ctx_send
from OA_Bot.ui.status_select_view import StatusSelectView


class Main(Cog_Extension):
    @commands.command()
    async def fsync(self, ctx: Context):
        synced = await self.bot.tree.sync()
        test_synced = 0
        for guild in TEST_GUILDS:
            test_synced += len(await self.bot.tree.sync(guild=guild))
        await ctx_send(ctx, f"已同步{len(synced)}條全域指令，{test_synced}條測試指令")

    @app_commands.command(description="載入模塊")
    @test_only
    @app_commands.check(is_owner)
    @app_commands.choices(cog_name=COG_CHOICES)
    async def load(
        self,
        interaction: discord.Interaction,
        cog_name: app_commands.Choice[str],
    ):
        await interaction.response.defer(ephemeral=True)
        cog_value = cog_name.value
        try:
            await self.bot.load_extension(f"OA_Bot.cogs.{cog_value}")
            await interaction.followup.send(f"已載入 {cog_value} 模塊")
        except Exception as e:
            await interaction.followup.send(f"載入模塊 {cog_value} 失敗，原因為: {e}")

    @app_commands.command(description="卸載模塊")
    @test_only
    @app_commands.check(is_owner)
    @app_commands.choices(cog_name=COG_CHOICES)
    async def unload(
        self,
        interaction: discord.Interaction,
        cog_name: app_commands.Choice[str],
    ):
        await interaction.response.defer(ephemeral=True)
        cog_value = cog_name.value
        try:
            await self.bot.unload_extension(f"OA_Bot.cogs.{cog_value}")
            await interaction.followup.send(f"已卸載 {cog_value} 模塊")
        except Exception as e:
            await interaction.followup.send(f"卸載模塊 {cog_value} 失敗，原因為: {e}")

    @app_commands.command(description="重新載入模塊")
    @test_only
    @app_commands.check(is_owner)
    @app_commands.choices(cog_name=COG_CHOICES)
    async def reload(
        self,
        interaction: discord.Interaction,
        cog_name: app_commands.Choice[str],
    ):
        await interaction.response.defer(ephemeral=True)
        cog_value = cog_name.value
        try:
            if cog_value == "*":
                for cog in COG_CHOICES:
                    if cog.value == "*":
                        continue
                    try:
                        await self.bot.unload_extension(f"OA_Bot.cogs.{cog.value}")
                        await self.bot.load_extension(f"OA_Bot.cogs.{cog.value}")
                    except:
                        pass

                await interaction.followup.send("已重新載入所有Cog")
            else:
                try:
                    await self.bot.unload_extension(f"OA_Bot.cogs.{cog_value}")
                except:
                    pass
                finally:
                    await self.bot.load_extension(f"OA_Bot.cogs.{cog_value}")

                await interaction.followup.send(f"已重新載入 {cog_value} 模塊")

        except commands.ExtensionNotLoaded as e:
            pass

        except Exception as e:
            await interaction.followup.send(
                f"重新載入模塊 {cog_value} 失敗，原因為: {e}", ephemeral=True
            )

    @app_commands.command(description="同步指令")
    @test_only
    @app_commands.check(is_owner)
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        synced = await self.bot.tree.sync()
        test_synced = 0
        for guild in TEST_GUILDS:
            test_synced += len(await self.bot.tree.sync(guild=guild))
        await interaction.followup.send(f"已同步{len(synced)}條全域指令，{test_synced}條測試指令")

    @app_commands.command(description="設置機器人狀態")
    @test_only
    @app_commands.check(is_owner)
    async def set_status(self, interaction: discord.Interaction):
        view = StatusSelectView(self.bot, self.data)
        await interaction.response.send_message(view=view, ephemeral=True)

    @app_commands.command(description="顯示ping值")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{round(self.bot.latency*1000)}毫秒", ephemeral=True
        )

    @app_commands.command(description="顯示幫助訊息")
    async def help(
        self,
        interaction: discord.Interaction,
        cog_name: Optional[Literal["id", "omi"]] = None,
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
