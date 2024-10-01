from disnake.ext import commands
from Utilities.staffchecks import admincheck
from Utilities.file_methods import search_file, GetProjectPath
import aiofiles, aiofiles.os as aios
from pathlib import Path

@commands.command(name='insertcode')
@admincheck()
async def insertcode(ctx, filename: str, line_number: int, *, code: str = None):
    code.replace("[e]", "    ")
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        if attachment.filename.endswith('.py'):
            content = await attachment.read()
            code = content.decode('utf-8', errors='replace')
        else:
            await ctx.send("Please attach a Python file.")
            return
    elif code is None:
        await ctx.send("Please provide the code to insert.")
        return
    try:
        path = Path(GetProjectPath())
        print(path)
        print(filename)
        filename = search_file(directory=path, search=filename)
        async with aiofiles.open(filename, 'r', encoding='utf-8') as file:
            lines = await file.readlines()

        if line_number > len(lines):
            await ctx.send("Line number exceeds the file length.")
            return

        lines.insert(line_number - 1, code.replace("[e]", "") + '\n') 

        async with aiofiles.open(filename, 'w', encoding='utf-8') as file:
            await file.writelines(lines)

        await ctx.send(f"Code inserted into {filename} at line {line_number}.")
    except Exception as e:
        await ctx.send(f"An error occurred uwu: {e}")

def setup_command(cog):
    cog.bot.add_command(insertcode)
    return insertcode
