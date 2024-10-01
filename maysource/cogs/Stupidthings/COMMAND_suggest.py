from disnake.ext import commands
import requests
import disnake
import random

@commands.command(name="suggest", help="Suggests into suggestions")
@commands.cooldown(1, 10, commands.BucketType.default)
async def suggest(ctx, *, suggestion):
    slt = ctx.bot.get_channel(1173959390785712168)
    await ctx.message.delete()
    embed = disnake.Embed(title=f"Suggestion by {ctx.author.display_name} ({ctx.author.name})", description=f"{suggestion}")
    mess = await slt.send(embed=embed)
    await mess.add_reaction("⬆️")
    await mess.add_reaction("⬇️")


def setup_command(cog):
    cog.bot.add_command(suggest)
    suggest.extras["example"] = "No Example Set"
    return suggest