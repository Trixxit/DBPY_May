from disnake.ext import commands
from pathlib import Path
from Utilities.file_methods import GetProjectPath
import aiofiles

maybot = None

@commands.command(name="addcog")
@commands.is_owner()
async def addcog(ctx, dir_name: str, inter_name: str, *, description: str):
    global maybot
    if inter_name in maybot.cogs or inter_name in maybot.all_commands:
        await ctx.send("Internal name already exists!")
    else:
        directory = Path(f"{GetProjectPath()}/cogs/{dir_name}")
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=False)
            content = ""
            async with aiofiles.open(f"{GetProjectPath()}/Plains/cogintro.txt", mode='r', encoding='utf-8') as file:
                content = await file.read()
            async with aiofiles.open(f"{GetProjectPath()}/cogs/{dir_name}/__init__.py", mode="w", encoding='utf-8') as file:
                await file.write(content.replace("NAME_TO_REPLACE", inter_name).replace("INSERT_DESC_HERE", f"\"{description}\"").replace("INSERT_FOLDER_HERE", f"\"{dir_name}\""))
                await file.flush()
            await ctx.send("Cog Group successfully added! Note: This group has not been loaded, nor does it have any commands.")

        else:
            await ctx.send("COG Directory already exists.")

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(addcog)
    return addcog