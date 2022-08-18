import json
import os

from discord.ext import commands

from core.check import is_owner
from core.tools import ctx_send

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix="~")

cmds = []
for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        cmds.append(filename[:-3])


@bot.event
async def on_ready():
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # channel = bot.get_channel(jdata["test-bot頻道"])
    # await channel.send("OA_Bot上線")
    print(f"[{now}] - OA_Bot上線")


@bot.command()
@is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cmds.{extension}")
    await ctx_send(ctx, f"已載入{extension}")


@bot.command()
@is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cmds.{extension}")
    await ctx_send(ctx, f"已卸載{extension}")


@bot.command()
@is_owner()
async def reload(ctx, *extensions):
    if "*" in extensions:
        for cmd in cmds:
            bot.unload_extension(f"cmds.{cmd}")
            bot.load_extension(f"cmds.{cmd}")
            await ctx_send(ctx, f"已重新載入{cmd}")
        await ctx.channel.purge(limit=len(cmds))
        await ctx_send(ctx, "已重新載入所有指令")
    else:
        extensions = set(extensions)
        error_list = set()
        for extension in extensions:
            try:
                bot.reload_extension(f"cmds.{extension}")
                await ctx_send(ctx, f"已重新載入{extension}")
            except commands.ExtensionNotLoaded:
                error_list.add(extension)
                await ctx_send(ctx, f"<{extension}不存在或無法載入>")

        extensions_len = len(extensions)
        if extensions_len > 1:
            extensions = extensions - error_list
            await ctx.channel.purge(limit=extensions_len)
            reload_msg = f"已重新載入{', '.join(extensions)}    " if extensions else ""
            cant_reload_msg = (
                ("<" + ", ".join(error_list) + "無法載入>") if error_list else ""
            )
            await ctx_send(ctx, f"{reload_msg}{cant_reload_msg}")


if __name__ == "__main__":
    for cmd in cmds:
        bot.load_extension(f"cmds.{cmd}")

    bot.run(jdata["TOKEN"])
