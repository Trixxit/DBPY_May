from disnake.ext import commands
from Utilities.staffchecks import staffguideCheck

@commands.command(name='uwu', description="uwu")
@staffguideCheck()
async def uwu(ctx):
    await ctx.send("uwu")

def setup_command(cog):
    cog.bot.add_command(uwu)
    return uwu