import json
import os

from discord.ext import commands

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix="~")


cmds = []
for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        cmds.append(filename[:-3])


@bot.event
async def on_ready():
    # channel = bot.get_channel(int(jdata["test-bot頻道"]))
    # await channel.send("OA_Bot上線")
    print("OA_Bot上線")


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cmds.{extension}")
    await ctx.send(f"```已載入{extension}```")


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cmds.{extension}")
    await ctx.send(f"```已卸載{extension}```")


@bot.command()
async def reload(ctx, *extensions):
    if extensions == "*":
        for cmd in cmds:
            bot.unload_extension(f"cmds.{cmd}")
            bot.load_extension(f"cmds.{cmd}")
            await ctx.send(f"```已重新載入{cmd}```")
        await ctx.channel.purge(limit=len(cmds))
        await ctx.send("```已重新載入所有指令```")
    else:
        for extension in extensions:
            bot.reload_extension(f"cmds.{extension}")
            await ctx.send(f"```已重新載入{extension}```")

        extensions_len = len(extensions)
        if extensions_len > 1:
            await ctx.channel.purge(limit=extensions_len)
            await ctx.send(f"```已重新載入{', '.join(extensions)}```")


for cmd in cmds:
    bot.load_extension(f"cmds.{cmd}")

if __name__ == "__main__":
    bot.run(jdata["TOKEN"])
