from functools import partial

from discord.ext.commands import Context


async def ctx_send(
    ctx: Context, *msg, color: str | None = None, sep: str = " ", **kwargs
):
    """
    傳送系統訊息

    一次只能傳送一行訊息,否則某些顏色顯示會出錯
    """
    msg = (str(m) for m in msg)
    msg = sep.join(msg)
    match color:
        case "normal" | "n":
            await ctx.send("```\n" + msg + "```", **kwargs)
        case "red" | "r":
            await ctx.send("```diff\n- " + msg + "```", **kwargs)
        case "orange" | "o":
            await ctx.send("```css\n[" + msg + "]```", **kwargs)
        case "yellow" | "y":
            await ctx.send("```fix\n" + msg + "```", **kwargs)
        case "green" | "g":
            await ctx.send("```diff\n+ " + msg + "```", **kwargs)
        case "lightGreen" | "lg":
            await ctx.send('```cs\n"' + msg + '"```', **kwargs)
        case "blue" | "b":
            await ctx.send("```ini\n[" + msg + "]```", **kwargs)
        case _:
            await ctx.send(msg, **kwargs)


async def ctx_send_normal(ctx: Context, *msg, sep: str = " ", **kwargs):
    ...


async def ctx_send_red(ctx: Context, *msg, sep: str = " ", **kwargs):
    ...


async def ctx_send_orange(ctx: Context, *msg, sep: str = " ", **kwargs):
    ...


async def ctx_send_yellow(ctx: Context, *msg, sep: str = " ", **kwargs):
    ...


async def ctx_send_green(ctx: Context, *msg, sep: str = " ", **kwargs):
    ...


async def ctx_send_lightGreen(ctx: Context, *msg, sep: str = " ", **kwargs):
    ...


async def ctx_send_blue(ctx: Context, *msg, sep: str = " ", **kwargs):
    ...


ctx_send_normal = partial(ctx_send, color="normal")
ctx_send_red = partial(ctx_send, color="red")
ctx_send_orange = partial(ctx_send, color="orange")
ctx_send_yellow = partial(ctx_send, color="yellow")
ctx_send_green = partial(ctx_send, color="green")
ctx_send_lightGreen = partial(ctx_send, color="lightGreen")
ctx_send_blue = partial(ctx_send, color="blue")
