from disnake.ext import commands
from Utilities.staffchecks import admincheck 

@commands.command(name="summon", description="[OBSOLETE] Summons Riku")
@admincheck()
async def summon(ctx, stri: str):
    global RikuSummon
    RikuSummon = True
    await ctx.send("Summoning <@306770167298392065>...")

def setup_command(cog):
    cog.bot.add_command(summon)
    return summon