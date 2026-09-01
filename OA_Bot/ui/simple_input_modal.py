from typing import Optional

import discord
from discord.ui import Modal, TextInput


class SimpleInputModal(Modal):
    """單一欄位、送出後即關閉的輸入用 Modal"""

    def __init__(
        self,
        title: str,
        label: str,
        *,
        placeholder: Optional[str] = None,
        default: Optional[str] = None,
        max_length: Optional[int] = None,
    ):
        super().__init__(title=title)
        self.answer = TextInput(
            label=label,
            placeholder=placeholder,
            default=default,
            max_length=max_length,
        )
        self.add_item(self.answer)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
