async def ctx_send(ctx, *msg, color=None, sep=' '):
    '''
    傳送系統訊息

    一次只能傳送一行訊息,否則某些顏色顯示會出錯
    '''
    msg = (str(m) for m in msg)
    msg = sep.join(msg)
    match color:
        case 'red' | 'r':
            await ctx.send("```diff\n- " + msg + "```")
        case 'orange' | 'o':
            await ctx.send("```css\n[" + msg + "]```")
        case 'yellow' | 'y':
            await ctx.send("```fix\n" + msg + "```")
        case 'green' | 'g':
            await ctx.send("```diff\n+ " + msg + "```")
        case 'lightGreen'| 'lg':
            await ctx.send('```cs\n"' + msg + '"```')
        case 'blue' | 'b':
            await ctx.send("```ini\n[" + msg + "]```")
        case _:
            await ctx.send("```\n" + msg + "```")