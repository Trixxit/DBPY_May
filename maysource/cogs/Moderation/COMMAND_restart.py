import disnake
from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import os
import sys

maybot = None

@commands.command(name="restart", description="Restart the bot")
@Anystaffcheck((1231831222930636800, 1180945644567941272))
async def restart(ctx):
    await ctx.send("Restarting the bot...")
    await maybot.close()
    os.execv(sys.executable, ['python'] + sys.argv)

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(restart)
    return restart