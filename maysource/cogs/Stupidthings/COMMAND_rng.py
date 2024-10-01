from disnake.ext import commands
import requests
import disnake
import random

@commands.command(name="rng", help="Randomly generates a number from a to b")
@commands.cooldown(1, 10, commands.BucketType.default)
async def rng(ctx, a: int = 1, b: int = 6):
    send = random.randint(a, b)
    title = f"Random number from {a} to {b}"
    desc = f"Random number is {send}"
    embed = disnake.Embed(title=title, description=desc)
    await ctx.send(embed=embed)


def setup_command(cog):
    cog.bot.add_command(rng)
    rng.extras["example"] = "No Example Set"
    return rng