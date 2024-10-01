from disnake.ext import commands

maybot = None

@commands.command(name='pfp', description="Sends may's pfp link")
async def maypfp(ctx):
    global maybot
    await ctx.send(maybot.user.avatar.url)
    await ctx.send(f"<{maybot.user.avatar.url}>")

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(maypfp)
    return maypfp