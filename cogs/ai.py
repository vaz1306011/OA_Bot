import discord
import openai
from discord import app_commands
from discord.ext import commands

from core.classes import Cog_Extension


class AI(Cog_Extension):
    """
    身分組指令群組
    """

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return

        if msg.channel.id == self.channel["ai問答"]:
            ans_msg = await msg.channel.send("OA_Bot正在思考...")
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"問題:{msg.content}\nOA_Bot:",
                temperature=0,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["問題:"],
            )

            answer = response["choices"][0]["text"]

            await ans_msg.edit(content=answer)

    AI_group = app_commands.Group(name="ai", description="AI指令群組")

    @AI_group.command(description="AI作畫")
    async def draw(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        import io

        import aiohttp

        response = openai.Image.create(prompt=text, n=1, size="1024x1024")
        image_urls = [url["url"] for url in response["data"]]

        images = []
        async with aiohttp.ClientSession() as session:
            for image_url in image_urls:
                async with session.get(image_url) as resp:
                    if resp.status != 200:
                        await interaction.followup.send(
                            f"Error: {resp.status} {resp.reason}"
                        )
                        return
                    image = io.BytesIO(await resp.read())
                    images.append(discord.File(image, filename=text + ".png"))

        await interaction.followup.send(text, files=images)

    @AI_group.command(description="AI問答")
    async def ask(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"問題:{text}\nOA_Bot:",
            temperature=0,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["問題:"],
        )

        answer = response["choices"][0]["text"]

        await interaction.followup.send(answer)

    @AI_group.command(description="AI聊天")
    async def chat(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f" 使用者:{text}\n OA_Bot:",
            temperature=0.9,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" 使用者:"],
        )

        answer = response["choices"][0]["text"]

        await interaction.followup.send(answer)


async def setup(bot: commands.Bot):
    print("已讀取AI")
    await bot.add_cog(AI(bot))


async def teardown(bot: commands.Bot):
    print("已移除AI")
    await bot.remove_cog("AI")
