from disnake.ext import commands
from Utilities.file_methods import find_file_and_extract_lines, getKG
from Utilities.staffchecks import staffCheck
import tempfile, aiofiles, disnake, aiofiles.os as aios

@commands.command(name='viewcode')
@staffCheck()
async def viewcode(ctx, filename: str, start: int, end: int):
    content = await find_file_and_extract_lines(filename, start, end)
    if not content:
         await ctx.send("File not Found")
         return
    print("test")
    content = f"```py\n{content.replace(getKG(),'(backtick)')}\n```"
    if len(content) < 1950:
            await ctx.send(content)
    else:
        try:
            temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False)
            temp_file_path = temp_file.name  # Store the file path to send
            temp_file.close()
            async with aiofiles.open(temp_file_path, 'w') as file:
                await file.write(content)
            await ctx.send(message="Here ya go!", file=disnake.File(temp_file_path, filename="output.py"))
            await aios.remove(temp_file_path)
        except disnake.HTTPException as e:
            print(f"HTTPException: Response: {e.response}, Message: {e.text}")
            try:
                 await aios.remove(temp_file_path)
            except:
                 pass
        except:
            print(f"An unexpected exception occurred: {e}")
            try:
                 await aios.remove(temp_file_path)
            except:
                 pass
             

def setup_command(cog):
    cog.bot.add_command(viewcode)
    return viewcode