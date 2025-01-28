from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension
from core.logger import logger


class Id(Cog_Extension):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        find_message_id = discord.app_commands.ContextMenu(
            name="查詢訊息id", callback=self.message
        )
        self.bot.tree.add_command(find_message_id)

    """
    id指令群組
    """

    async def message(self, interaction: discord.Interaction, message: discord.Message):
        """查詢訊息id

        Args:
            interaction (discord.Interaction): interaction
            message (str): 訊息
            n (int): 第幾個訊息
        """
        await interaction.response.send_message(
            f"此訊息的ID為: {message.id}", ephemeral=True
        )

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
    async def channel(
        self,
        interaction: discord.Interaction,
        channel: (
            discord.TextChannel
            | discord.VoiceChannel
            | discord.StageChannel
            | discord.CategoryChannel
            | None
        ) = None,
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
    async def guild(self, interaction: discord.Interaction):
        """查詢伺服器id

        Args:
            interaction (discord.Interaction): interaction
        """
        await interaction.response.send_message(
            f"{interaction.guild} 伺服器的ID為: {interaction.guild.id}", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Id(bot))
    logger.info("已讀取 Id 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("Id")
    logger.info("已移除 Id 模塊")
