from disnake.ext import commands
from pathlib import Path
from Utilities.file_methods import GetProjectPath
import aiofiles

maybot = None

@commands.command(name="addcmd")
@commands.is_owner()
async def addcmd(ctx, dir_name: str, inter_name: str, cmd_name: str, *, description: str):
    global maybot
    if inter_name in maybot.cogs or inter_name in maybot.all_commands:
        await ctx.send("Internal name already exists!")
    else:
        directory = Path(f"{GetProjectPath()}/cogs/{dir_name}")
        if directory.exists():
            content = ""
            async with aiofiles.open(f"{GetProjectPath()}/Plains/commandintro.txt", mode='r', encoding='utf-8') as file:
                content = await file.read()
            async with aiofiles.open(f"{GetProjectPath()}/cogs/{dir_name}/COMMAND_{inter_name}.py", mode="w", encoding='utf-8') as file:
                await file.write(content.replace("INSERT_NAME_HERE", cmd_name).replace("INSERT_INTER_HERE", inter_name).replace("INSERT_DESC_HERE", description))
                await file.flush()
            await ctx.send(f"Command `{cmd_name}` successfully added to cog `{dir_name}`! Note: This command has not been loaded.")

        else:
            await ctx.send("COG Directory does not exist. Please use `>>add_cog (dir_name) (inter_name)` to create one")

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(addcmd)
    return addcmd