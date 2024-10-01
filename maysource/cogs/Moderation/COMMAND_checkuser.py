from disnake.ext import commands
from Utilities.staffchecks import staffguideCheck
import disnake

@commands.command(name='CU', description="Outputs the avatar of a user")
@staffguideCheck()
async def checkuser(ctx, mem: disnake.Member):
    await ctx.send(mem.avatar)

def setup_command(cog):
    cog.bot.add_command(checkuser)
    return checkuser