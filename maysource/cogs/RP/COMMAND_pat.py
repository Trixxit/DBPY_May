from disnake.ext import commands
import disnake
import random
from Utilities.discord_utils import sanmes

pat_gifs = [
    "https://tenor.com/6i3n.gif",
    "https://tenor.com/MLKi.gif",
    "https://tenor.com/Nj5e.gif",
    "https://tenor.com/YAN5.gif",
    "https://tenor.com/xjJl.gif",
    "https://tenor.com/LgfZ.gif",
    "https://tenor.com/vNjW.gif",
    "https://tenor.com/T56F.gif",
    "https://tenor.com/KuTJ.gif",
    "https://tenor.com/zS41.gif"
]

@commands.command(name='pat', description="pat!")
@commands.cooldown(2, 10, commands.BucketType.default)
async def pat(ctx, mem: disnake.Member):
    if (mem.id == ctx.author.id):
        await ctx.send("I pet you instead, *pat pat* ^^")
    else:
        await ctx.send(sanmes(f"{ctx.author.display_name} pats {mem.display_name}!!!"))
        await ctx.send(random.choice(pat_gifs))


def setup_command(cog):
    cog.bot.add_command(pat)
    pat.extras["example"] = "No Example Set"
    return pat