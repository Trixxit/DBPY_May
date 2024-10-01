from disnake.ext import commands
import disnake
import random
from Utilities.discord_utils import sanmes

pat_gifs = [
    "https://media1.tenor.com/m/x8v1oNUOmg4AAAAd/rickroll-roll.gif"
]

@commands.command(name='unpat', description="unpat!")
@commands.cooldown(2, 10, commands.BucketType.default)
async def unpat(ctx, mem: disnake.Member):
    if (mem.id == ctx.author.id):
        await ctx.send("I unpet you instead, *unpat unpat* ^^")
    else:
        await ctx.send(sanmes(f"{ctx.author.display_name} unpats {mem.display_name}!!!"))
        await ctx.send(random.choice(pat_gifs))


def setup_command(cog):
    cog.bot.add_command(unpat)
    unpat.extras["example"] = "No Example Set"
    return unpat