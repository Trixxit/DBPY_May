import disnake
from disnake.ext import commands
import asyncio
import time as tt

@commands.command(name='remind')
async def remind(ctx, time: str, *, message: str):
    multiply = 1
    for i in time:
        if i == "s":
            multiply = 1
        elif i == "m":
            multiply = 60
        elif i == "h":
            multiply = 60 * 60
        elif i == "d":
            multiply = 60 * 60 * 24
    timed = time[:len(time)-1]
    print(timed)
    if timed.isdigit():

        reminder_time = int(tt.time()) + int(timed)*multiply
        embed = disnake.Embed(title=f"{ctx.author.display_name} Created Reminder", description=f"Reminder set! I will remind you in {time} (at <t:{reminder_time}:D> <t:{reminder_time}:T> which is/was <t:{reminder_time}:R>)")
        await ctx.send(embed=embed)
        await asyncio.sleep(int(timed)*multiply)
        message = message.replace("@", "\@")
        message = message.replace(".", "\.")
        message = message.replace("/", "\/")
        embed = disnake.Embed(title=f"{ctx.author.display_name} Reminder!", description=f"{message}")
        await ctx.send(f"<@{ctx.author.id}>", embed=embed)
        return
    else:
        await ctx.send(f"Invalid time {time}")

def setup_command(cog):
    cog.bot.add_command(remind)
    return remind