from disnake.ext import commands
from Utilities.staffchecks import admincheck
import disnake
import asyncio

@commands.command(name='murder', aliases=["murder.", "murdering"], description="murder")
@admincheck()
async def murder(ctx, murder: disnake.Member):
    while True:
        try:
            message = await ctx.send(murder.mention)
            await message.delete()
        except:
            await asyncio.sleep(5)

def setup_command(cog):
    cog.bot.add_command(murder)
    return murder