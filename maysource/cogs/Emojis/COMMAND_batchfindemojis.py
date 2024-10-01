from disnake.ext import commands

@commands.command(name='batchfindemojis', description="Gets emojis... in a batch!")
async def batchfindemojis(ctx):
    print("Blank command")


def setup_command(cog):
    cog.bot.add_command(batchfindemojis)
    batchfindemojis.extras["example"] = "No Example Set"
    return batchfindemojis