from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
from pathlib import Path
from Utilities.file_methods import GetProjectPath

maybot = None

@commands.command(name="load")
@Anystaffcheck((1196465778438963392, 1231831222930636800, 1180945644567941272))
async def hotload(ctx, name: str):
    global maybot
    dir = f"{GetProjectPath()}/cogs/{name}"
    print(dir)
    if Path(dir).exists() and Path(dir).is_dir():
        initfile = Path(dir + "/__init__.py")
        if initfile.is_file():
            try:
                maybot.load_extension(f'cogs.{name}')
                await ctx.send(f'Cog group `{name}` loaded.')
            except Exception as e:
                    await ctx.send(f'Error occurred: {e}')
        else:
             await ctx.send("No `__init__` file found in specified directory.")
    else:
        await ctx.send("The specified directory does not exist.")


def setup_command(cog):
     global maybot
     maybot = cog.bot
     cog.bot.add_command(hotload)
     return hotload