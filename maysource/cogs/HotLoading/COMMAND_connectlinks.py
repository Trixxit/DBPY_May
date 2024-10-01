from disnake.ext import commands
from Utilities.file_methods import GetProjectPath
from Utilities.staffchecks import admincheck
from pathlib import Path

@commands.command(name='connectcogs')
@admincheck()
async def connectlinks(ctx):
    path = f"{GetProjectPath()}/cogs"
    for dir_entry in Path(path).iterdir():
        if dir_entry.is_dir():
            dir_name = dir_entry.name
            try:
                maybot.load_extension(f'cogs.{dir_name}')
                await ctx.send(f'Cog group `{dir_name}` loaded.')
            except Exception as e:
                await ctx.send(f"Failed to load cog subdirectory `{dir_name}`")
                print(f"Failed to load cog subdirectory `{dir_name}`: {e}")

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(connectlinks)
    return connectlinks
