from disnake.ext import commands

@commands.command(name='__blacklist', description="Blacklist a member from something!")
async def allblacklist(ctx):
    print("Blank command")


def setup_command(cog):
    cog.bot.add_command(allblacklist)
    allblacklist.extras["example"] = "No Example Set"
    return allblacklist