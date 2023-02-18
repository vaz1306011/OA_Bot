from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from core.check import is_owner
from core.classes import Cog_Extension


class Id(Cog_Extension):

    """
    id指令群組
    """

    id_group = app_commands.Group(name="id", description="id指令群組")

    @id_group.command()
    async def member(
        self,
        interaction: discord.Interaction,
        member: Optional[discord.Member] = None,
    ):
        """查詢成員id

        Args:
            interaction (discord.Interaction): interaction
            member (Optional[discord.Member], optional): 成員(預設為自己)
        """
        if member is not None:
            await interaction.response.send_message(
                f"{member} 成員的ID為: {member.id}", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"你的ID為: {interaction.user.id}", ephemeral=True
            )

    @id_group.command()
    async def role(self, interaction: discord.Interaction, role: discord.Role):
        """查詢身分組id

        Args:
            interaction (discord.Interaction): interaction
            role (discord.Role): 身分組
        """
        await interaction.response.send_message(
            f"{role} 身分組的ID為: {role.id}", ephemeral=True
        )

    @id_group.command()
    async def message(self, interaction: discord.Interaction, message: str, n: int):
        """查詢訊息id

        Args:
            interaction (discord.Interaction): interaction
            message (str): 訊息
            n (int): 第幾個訊息
        """
        # TODO怎麼取得訊息id
        ...

    @id_group.command()
    async def channel(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel
        | discord.VoiceChannel
        | discord.StageChannel
        | discord.CategoryChannel
        | None = None,
    ):
        """查詢頻道id

        Args:
            interaction (discord.Interaction): interaction
            channel (discord.TextChannel | discord.VoiceChannel | discord.StageChannel | discord.CategoryChannel | None, optional): 頻道(預設為當前頻道)
        """
        if channel is None:
            channel = interaction.channel
        await interaction.response.send_message(
            f"{channel.name} 頻道的ID為: {channel.id}", ephemeral=True
        )

    @id_group.command()
    @app_commands.check(is_owner)
    async def guild(self, interaction: discord.Interaction):
        """查詢伺服器id

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.send_message(
            f"{interaction.guild} 伺服器的ID為: {interaction.guild.id}", ephemeral=True
        )


async def setup(bot: commands.Bot):
    print("已讀取Id")
    await bot.add_cog(Id(bot))


async def teardown(bot: commands.Bot):
    print("已移除Id")
    await bot.remove_cog("Id")
