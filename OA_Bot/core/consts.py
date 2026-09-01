import discord
from discord import app_commands

# 測試伺服器，僅供測試用的指令會被限制只註冊到這些伺服器
TEST_GUILD_IDS = [758330839691558974, 654271255066968074]
TEST_GUILDS = [discord.Object(id=guild_id) for guild_id in TEST_GUILD_IDS]

# 裝飾在指令上，讓該指令只註冊到測試伺服器
test_only = app_commands.guilds(*TEST_GUILDS)
