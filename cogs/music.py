import asyncio
import functools
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Dict

import discord
import yt_dlp
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ui import Modal, Select, TextInput, View
from discord.voice_client import VoiceClient

from core.classes import Cog_Extension
from core.logger import logger

# YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
YDL_OPTIONS = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,  # 關閉輸出日志
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
    "usenetrc": True,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


@dataclass
class MusicData:
    name: str
    url: str
    webpage_url: str
    order: discord.Member | None = None


@dataclass
class PlayList:
    now_playing: MusicData | None = None
    play_list: deque[MusicData] = deque()

    def get_next(self) -> MusicData | None:
        self.now_playing = self.play_list.popleft()
        return self.now_playing

    def append(self, music: MusicData) -> "PlayList":
        self.play_list.append(music)
        return self

    def insert(self, music: MusicData, index: int) -> "PlayList":
        """插入音樂到播放清單中

        Args:
            index (int): 插入的位置
            music (MusicData): 音樂資料

        play_list = [1, 2, 3, 4, 5]

        index = 0 -> [x, 1, 2, 3, 4, 5]

        index = 1 -> [x, 1, 2, 3, 4, 5]

        index = 2 -> [1, x, 2, 3, 4, 5]

        index = 7 -> [1, 2, 3, 4, 5, x]
        """

        index = sorted([1, index, len(self.play_list) + 1])[1]
        self.play_list.insert(index - 1, music)
        return self

    def clear_play_list(self) -> "PlayList":
        self.play_list.clear()
        return self

    def clear_all(self) -> "PlayList":
        self.now_playing = None
        self.play_list.clear()
        return self

    def is_empty(self) -> bool:
        return self.now_playing is None and len(self.play_list) == 0


class Music(Cog_Extension):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.ytdl = yt_dlp.YoutubeDL(YDL_OPTIONS)
        self.play_lists: Dict[int, PlayList] | None = dict()  # 伺服器id:播放清單
        self.thread_pool = ThreadPoolExecutor(max_workers=2)

    def __get_play_list(self, guild_id: int) -> PlayList:
        """獲取伺服器的播放清單

        Args:
            guild_id (int): 伺服器id

        Returns:
            PlayList: 播放清單
        """
        return self.play_lists.setdefault(guild_id, PlayList())

    async def __connect(self, interaction: discord.Interaction) -> VoiceClient | None:
        """加入語音頻道

        Args:
            interaction (discord.Interaction): 交互事件
        """
        if not interaction.user.voice:
            await interaction.followup.send("您不在任何語音頻道中")
            return None

        channel = interaction.user.voice.channel

        logger.debug(f"嘗試加入 {channel.name} 語音頻道...")

        try:
            vc = await asyncio.wait_for(
                channel.connect(timeout=20.0, reconnect=True), timeout=25.0
            )
            logger.debug("成功加入語音頻道")

            self.__get_play_list(interaction.guild_id)
            await interaction.followup.send(f"已加入 {channel.mention} 頻道")
            return vc

        except asyncio.TimeoutError:
            logger.error("語音連線超時，請檢查網路環境或 Intents 設定。")
            await interaction.followup.send("連線超時，請稍後再試。")
            return None
        except Exception as e:
            logger.error(f"加入語音頻道發生錯誤: {e}", exc_info=True)
            await interaction.followup.send(f"無法加入頻道: {e}")
            return None

    def __play_next(self, guild: discord.Guild):
        """播放下一首歌曲

        Args:
            guild (discord.Guild): 伺服器
        """
        music = self.__get_play_list(guild.id).get_next()
        if music is None:
            return

        vc: VoiceClient = guild.voice_client
        vc.play(
            discord.FFmpegPCMAudio(
                music.url,
                **FFMPEG_OPTIONS,
            ),
            after=lambda e: self.__play_next(guild),
        )

    async def __get_music(self, url: str, order: discord.Member = None) -> MusicData:
        """獲取音樂資料

        Args:
            url (str): youtube網址

        Returns:
            MusicData: 音樂資料

        """
        # with yt_dlp.YoutubeDL(YDL_OPTIONS) as ytdl:
        #     info = ytdl.extract_info(url, download=False)
        #     return MusicData(info["title"], info["url"], url)

        info = await self.bot.loop.run_in_executor(
            self.thread_pool,
            functools.partial(self.ytdl.extract_info, url, download=False),
        )

        if "entries" in info:
            info = info["entries"][0]

        return MusicData(info["title"], info["url"], info["webpage_url"], order)

    async def __queue(self, interaction: discord.Interaction, url: str, index: int):
        """加入音樂到播放清單中

        Args:
            interaction (discord.Interaction): 交互事件
            url (str): youtube網址
            index (int): 插入的位置
        """
        msg = await interaction.followup.send("讀取音樂中...", wait=True)

        music = await self.__get_music(url, interaction.user)

        play_list = self.__get_play_list(interaction.guild_id)
        if index is None:
            play_list.append(music)
        else:
            play_list.insert(music, index)

        await msg.edit(
            content=f"[**{music.name}**]({music.webpage_url}) 已加入到待播清單中"
        )

    music_group = app_commands.Group(name="music", description="music指令群組")

    @music_group.command()
    async def gui(self, interaction: discord.Interaction):
        """音樂播放器

        Args:
            interaction (discord.Interaction): 交互事件
        """
        # TODO音樂播放器
        ...

    @music_group.command()
    async def disconnect(self, interaction: discord.Interaction):
        """離開語音頻道

        Args:
            interaction (discord.Interaction): 交互事件
        """
        if not interaction.guild.voice_client:
            await interaction.response.send_message(
                "機器人不在任何語音頻道中", ephemeral=True
            )
            return

        self.play_lists.pop(interaction.guild.id).clear_all()
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("已離開語音頻道")

    @music_group.command()
    async def play(
        self, interaction: discord.Interaction, music: str, index: int = None
    ):
        """播放音樂

        Args:
            interaction (discord.Interaction): 交互事件
            music (str): 音樂名稱或網址
            index (int, optional): 插入的位置.
        """
        await interaction.response.defer()

        if not interaction.user.voice:
            await interaction.followup.send("你不在任何語音頻道中", ephemeral=True)
            return

        vc = interaction.guild.voice_client or await self.__connect(interaction)

        if vc is None:
            await interaction.followup.send("無法加入語音頻道")
            return

        elif interaction.user.voice.channel.id != vc.channel.id:
            await interaction.followup.send(f"滾去 {vc.channel.mention} 聽歌")
            return

        await self.__queue(interaction, music, index)
        if not vc.is_playing():
            self.__play_next(interaction.guild)

    @music_group.command()
    async def stop(self, interaction: discord.Interaction):
        """停止播放

        Args:
            interaction (discord.Interaction): 交互事件
        """
        vc: VoiceClient = interaction.guild.voice_client
        vc.stop()
        await interaction.response.send_message(f"停止")

    @music_group.command()
    async def pause(self, interaction: discord.Interaction):
        """暫停播放

        Args:
            interaction (discord.Interaction): 交互事件
        """
        vc: VoiceClient = interaction.guild.voice_client
        vc.pause()
        await interaction.response.send_message(f"暫停")

    @music_group.command()
    async def resume(self, interaction: discord.Interaction):
        """繼續播放

        Args:
            interaction (discord.Interaction): 交互事件
        """
        vc: VoiceClient = interaction.guild.voice_client
        vc.resume()
        await interaction.response.send_message(f"繼續")

    @music_group.command()
    async def skip(self, interaction: discord.Interaction):
        """跳過目前播放的歌曲

        Args:
            interaction (discord.Interaction): 交互事件
        """
        vc: VoiceClient = interaction.guild.voice_client
        vc.stop()
        await interaction.response.send_message(f"跳過")

    @music_group.command()
    async def play_list(self, interaction: discord.Interaction):
        """顯示播放清單

        Args:
            interaction (discord.Interaction): 交互事件
        """
        await interaction.response.defer(ephemeral=True)
        play_list = self.__get_play_list(interaction.guild_id)
        if play_list.is_empty():
            await interaction.followup.send("播放清單是空的")
            return

        now_playing = play_list.now_playing
        embed = discord.Embed(title="播放清單", color=0xE67E22)
        embed.add_field(
            name="",
            value=f"🔴正在播放 - [**{now_playing.name}**]({now_playing.webpage_url}) - {now_playing.order.mention}",
            inline=False,
        )
        for index, music in enumerate(play_list.play_list):
            embed.add_field(
                name="",
                value=f"`{index+2}.` [**{music.name}**]({music.webpage_url}) - {music.order.mention}",
                inline=False,
            )

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
    logger.info("已讀取 Music 模塊")


async def teardown(bot: commands.Bot):
    await bot.remove_cog("Music")
    logger.info("已移除 Music 模塊")
