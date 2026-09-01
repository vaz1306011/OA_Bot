from discord import Interaction, app_commands


class Tree(app_commands.CommandTree):
    async def on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError, /
    ) -> None:
        interaction.client.dispatch("app_command_error", interaction, error)
