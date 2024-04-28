import discord
from discord import app_commands
from discord.ext import commands

from core.check import is_owner
from core.classes import Cog_Extension
from core.logger import logger


class Role(Cog_Extension):
    """
    身分組指令群組
    """

    role_group = app_commands.Group(name="role", description="身分組指令群組")

    @role_group.command(description="給定使用者身分組")
    async def add(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role,
    ):
        await member.add_roles(role)
        await interaction.response.send_message(
            f"已給予 {member} {role} 身分組", ephemeral=True
        )

    @role_group.command(description="移除使用者身分組")
    async def remove(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role,
    ):
        await member.remove_roles(role)
        await interaction.response.send_message(
            f"已移除 {member} {role} 身分組", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Role(bot))
    logger.info("已讀取 Role 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("Role")
    logger.info("已移除 Role 模塊")
