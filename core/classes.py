import json

import discord
from discord import ButtonStyle, Interaction
from discord.ext import commands
from discord.ui import Button, View


class Cog_Extension(commands.Cog):
    with open("data.json", "r", encoding="utf8") as f:
        data = json.load(f)

    id: dict = data["id"]
    role: dict = data["role"]
    channel: dict = data["channel"]
    URL: dict = data["URL"]

    class Role_button(Button):
        def __init__(
            self, role_id, label: str, style: ButtonStyle, emoji: str, **kwargs
        ) -> None:
            super().__init__(label=label, style=style, emoji=emoji, **kwargs)
            self.role_id = role_id

        async def callback(self, interaction: Interaction) -> None:
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

    class VOWView(View):
        def __init__(self, n: int, timeout=None) -> None:
            super().__init__(timeout=timeout)
            self.n = n
            self.clicked_people = dict()

            V = Button(label="剪刀", emoji="✌🏽")
            O = Button(label="石頭", emoji="✊🏽")
            W = Button(label="布", emoji="✋🏽")

            async def check_end(interaction: Interaction):
                if len(self.clicked_people) >= self.n:
                    await interaction.message.delete()

                    choices = set(self.clicked_people.values())
                    winner = None
                    if len(choices) not in (1, 3):
                        if "✌🏽剪刀" in choices:
                            if "✊🏽石頭" in choices:
                                winner = "✊🏽石頭"
                            else:
                                winner = "✌🏽剪刀"
                        else:
                            winner = "✋🏽布"

                    description = ""
                    for user_id, choice in self.clicked_people.items():
                        user = interaction.guild.get_member(user_id)
                        description += f"{user.mention}：{choice}"
                        description += " 👑" if choice == winner else ""
                        description += "\n"

                    embed = discord.Embed(title="猜拳結果", description=description.strip())
                    await interaction.channel.send(embed=embed)

            async def V_cb(interaction: Interaction):
                await interaction.response.defer()
                self.clicked_people[interaction.user.id] = "✌🏽剪刀"
                await check_end(interaction)

            async def O_cb(interaction: Interaction):
                await interaction.response.defer()
                self.clicked_people[interaction.user.id] = "✊🏽石頭"
                await check_end(interaction)

            async def W_cb(interaction: Interaction):
                await interaction.response.defer()
                self.clicked_people[interaction.user.id] = "✋🏽布"
                await check_end(interaction)

            V.callback = V_cb
            O.callback = O_cb
            W.callback = W_cb

            for choice in (V, O, W):
                self.add_item(choice)

    def __init__(self, bot: commands.Bot):
        self.bot = bot
