import discord
from discord.ext import commands


class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ctx_send(self, ctx, msg, color=None):
        match color:
            case 'red':
                await ctx.send("```" + msg + "```", embed=discord.Embed(color=0xFF0000))
            case 'green':
                await ctx.send("```" + msg + "```", embed=discord.Embed(color=0x00FF00))
            case 'blue':
                await ctx.send("```" + msg + "```", embed=discord.Embed(color=0x0000FF))
            case _:
                await ctx.send("```" + msg + "```")
