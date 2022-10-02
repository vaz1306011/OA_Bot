import json

import discord
from discord.ext import commands
from discord.ui import Button


class Cog_Extension(commands.Cog):
    with open("data.json", "r", encoding="utf8") as f:
        data = json.load(f)

    id: dict = data["id"]
    role: dict = data["role"]
    channel: dict = data["channel"]

    class Role_button(Button):
        def __init__(self, role_id, **kwargs):
            super().__init__(**kwargs)
            self.role_id = role_id

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer()
            role = interaction.guild.get_role(self.role_id)
            if role is None:
                raise commands.BadArgument("找不到身分組")

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

    def __init__(self, bot: commands.Bot):
        self.bot = bot
