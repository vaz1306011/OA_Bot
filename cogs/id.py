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

    @id_group.command(description="成員id")
    async def member(
        self,
        interaction: discord.Interaction,
        member: Optional[discord.Member] = None,
    ):
        if member is not None:
            await interaction.response.send_message(
                f"{member} 成員的ID為: {member.id}", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"你的ID為: {interaction.user.id}", ephemeral=True
            )

    @id_group.command(description="身分組id")
    async def role(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.send_message(
            f"{role} 身分組的ID為: {role.id}", ephemeral=True
        )

    @id_group.command(description="顯示頻道id")
    async def channel(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel
        | discord.VoiceChannel
        | discord.StageChannel
        | discord.CategoryChannel
        | None = None,
    ):
        if channel is None:
            channel = interaction.channel
        await interaction.response.send_message(
            f"{channel.name} 頻道的ID為: {channel.id}", ephemeral=True
        )

    @id_group.command(description="顯示伺服器的id")
    @app_commands.check(is_owner)
    async def guild(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{interaction.guild} 伺服器的ID為: {interaction.guild.id}", ephemeral=True
        )


async def setup(bot: commands.Bot):
    print("已讀取Id")
    await bot.add_cog(Id(bot))


async def teardown(bot: commands.Bot):
    print("已移除Id")
    await bot.remove_cog("Id")
