from disnake.ext import commands
import disnake
import random
from Utilities.discord_utils import sanmes

hug_gifs = [
    "https://tenor.com/G08M.gif",
    "https://tenor.com/vksq.gif",
    "https://tenor.com/7Wko.gif",
    "https://tenor.com/FQNP.gif",
    "https://tenor.com/ETCF.gif",
    "https://tenor.com/UJpF.gif",
    "https://tenor.com/QWw1.gif",
    "https://tenor.com/uIwE.gif",
    "https://tenor.com/xNZi.gif",
    "https://tenor.com/1jRF.gif"
]

@commands.command(name='hug', description="hug!")
@commands.cooldown(2, 10, commands.BucketType.default)
async def hug(ctx, mem: disnake.Member):
    if (mem.id == ctx.author.id):
        await ctx.send("A-Are you okay, " + ctx.author.display_name + "...? ;-;")
    else:
        await ctx.send(sanmes(f"{ctx.author.display_name} hugs {mem.display_name}!!!"))
        await ctx.send(random.choice(hug_gifs))


def setup_command(cog):
    cog.bot.add_command(hug)
    hug.extras["example"] = "No Example Set"
    return hug