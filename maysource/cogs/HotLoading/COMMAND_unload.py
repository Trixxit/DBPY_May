from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck, maycest

maybot = None

@commands.command(name="unload")
@Anystaffcheck((maycest))
async def hotunload(ctx, name: str):
    global maybot
    try:
        maybot.unload_extension(f'cogs.{name}')
        await ctx.send(f'Cog group `{name}` unloaded.')
    except Exception as e:
            await ctx.send(f'Error occurred: {e}')

def setup_command(cog):
     global maybot
     maybot = cog.bot
     cog.bot.add_command(hotunload)
     return hotunload