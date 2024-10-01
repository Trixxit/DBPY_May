from disnake.ext import commands
from Utilities.staffchecks import admincheck
from Utilities.file_methods import search_file, GetProjectPath
import aiofiles
from pathlib import Path

@commands.command(name='replin', description="Replace a line infile with a new line")
@admincheck()
async def replaceline(ctx, filename: str, line_number: int, *, new_code: str):
    if not new_code:
        await ctx.send("Please provide the code to replace.")
        return

    new_code = new_code.replace("[e]", "    ")
    try:
        path = Path(GetProjectPath())
        filename = search_file(directory=path, search=filename)
        
        async with aiofiles.open(filename, 'r', encoding='utf-8') as file:
            lines = await file.readlines()

        if 1 <= line_number <= len(lines):
            lines[line_number - 1] = new_code + '\n'
            async with aiofiles.open(filename, 'w', encoding='utf-8') as file:
                await file.writelines(lines)
            await ctx.send(f"Line `{line_number}` in `{filename}` has been replaced.")
        else:
            await ctx.send("Line number is out of file's range.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

def setup_command(cog):
    cog.bot.add_command(replaceline)
    return replaceline