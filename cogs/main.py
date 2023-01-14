import enum
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

import bot
from core.check import is_owner
from core.classes import Cog_Extension


class Main(Cog_Extension):
    Cogs = enum.Enum("Cog", {cog: cog for cog in (["*"] + bot.cogs)})

    @app_commands.command(description="載入模塊")
    @app_commands.check(is_owner)
    async def load(self, interaction: discord.Interaction, cog_name: Cogs):
        await interaction.response.defer(ephemeral=True)
        cog_name = cog_name.value
        try:
            await self.bot.load_extension(f"cogs.{cog_name}")
            await interaction.followup.send(f"已載入 {cog_name} 模塊", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(
                f"載入模塊 {cog_name} 失敗，原因為: {e}", ephemeral=True
            )

    @app_commands.command(description="卸載模塊")
    @app_commands.check(is_owner)
    async def unload(self, interaction: discord.Interaction, cog_name: Cogs):
        await interaction.response.defer(ephemeral=True)
        cog_name = cog_name.value
        try:
            await self.bot.unload_extension(f"cogs.{cog_name}")
            await interaction.followup.send(f"已卸載 {cog_name} 模塊", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(
                f"卸載模塊 {cog_name} 失敗，原因為: {e}", ephemeral=True
            )

    @app_commands.command(description="重新載入模塊")
    @app_commands.check(is_owner)
    async def reload(
        self,
        interaction: discord.Interaction,
        cog_name: Cogs,
    ):
        await interaction.response.defer(ephemeral=True)
        cog_name = cog_name.value
        try:
            if cog_name == "*":
                for cmd in bot.cogs:
                    try:
                        await self.bot.unload_extension(f"cogs.{cmd}")
                        await self.bot.load_extension(f"cogs.{cmd}")
                    except:
                        pass

                await interaction.followup.send("已重新載入所有Cog", ephemeral=True)
            else:
                try:
                    await self.bot.unload_extension(f"cogs.{cog_name}")
                except:
                    pass
                finally:
                    await self.bot.load_extension(f"cogs.{cog_name}")

                await interaction.followup.send(f"已重新載入 {cog_name} 模塊", ephemeral=True)

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
        synced_oa = await self.bot.tree.sync(guild=discord.Object(self.GUILD["老屁股"]))
        if interaction.guild_id == self.GUILD["老屁股"]:
            await interaction.followup.send(
                f"已同步{len(synced)}條指令，{len(synced_oa)}條OA指令", ephemeral=True
            )
        else:
            await interaction.followup.send(f"已同步{len(synced)}條指令", ephemeral=True)

    @app_commands.command(description="設置機器人狀態")
    @app_commands.check(is_owner)
    async def set_status(
        self,
        interaction: discord.Interaction,
        status: Literal["線上", "閒置", "請勿打擾", "離線"],
        activity: Literal["正在玩", "正在直播", "正在看", "正在聽", "競爭"] | None = None,
        name: str | None = None,
        url: str | None = None,
    ):
        await interaction.response.defer(ephemeral=True)
        if activity is not None:
            match activity:
                case "正在玩":
                    activity = discord.Game(name=name)
                case "正在直播":
                    activity = discord.Activity(
                        name=name, type=discord.ActivityType.streaming, url=url
                    )
                case "正在看":
                    activity = discord.Activity(
                        name=name, type=discord.ActivityType.watching
                    )
                case "正在聽":
                    activity = discord.Activity(
                        name=name, type=discord.ActivityType.listening
                    )
                case "競爭":
                    activity = discord.Activity(
                        name=name, type=discord.ActivityType.competing
                    )

        match status:
            case "線上":
                await self.bot.change_presence(
                    status=discord.Status.online, activity=activity
                )
            case "閒置":
                await self.bot.change_presence(
                    status=discord.Status.idle, activity=activity
                )
            case "請勿打擾":
                await self.bot.change_presence(
                    status=discord.Status.dnd, activity=activity
                )
            case "離線":
                await self.bot.change_presence(
                    status=discord.Status.offline, activity=activity
                )

        await interaction.followup.send(f"已設定狀態", ephemeral=True)

    @app_commands.command(description="顯示ping值")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{round(self.bot.latency*1000)}毫秒", ephemeral=True
        )


async def setup(bot: commands.Bot):
    print("已讀取Main")
    await bot.add_cog(Main(bot))


async def teardown(bot: commands.Bot):
    print("已移除Main")
    await bot.remove_cog("Main")
