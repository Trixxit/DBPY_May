from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck

maybot = None

@commands.command(name="reload")
@Anystaffcheck((1231831222930636800,1180945644567941272))
async def hotreload(ctx, name: str):
    global maybot
    try:
        maybot.unload_extension(f'cogs.{name}')
        maybot.load_extension(f'cogs.{name}')
        await ctx.send(f'Cog group `{name}` reloaded.')
    except:
            try:
                maybot.unload_extension(f'{name}')
                maybot.load_extension(f'{name}')
                await ctx.send(f'Extension `{name}` reloaded.')
            except Exception as e:
                await ctx.send(f'Error occurred: {e}')

def setup_command(cog):
     global maybot
     maybot = cog.bot
     cog.bot.add_command(hotreload)
     return hotreload