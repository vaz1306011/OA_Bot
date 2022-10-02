async def ctx_send(ctx, *msg, color=None, sep=" ", **kwargs):
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
