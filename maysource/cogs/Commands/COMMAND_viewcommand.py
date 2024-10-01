from disnake.ext import commands
from disnake import File
from Utilities.file_methods import FCF
from Utilities.staffchecks import staffCheck
from Utilities.file_methods import extract_command_code, getKG
import aiofiles

maybot = None

@commands.command(name='viewcmd')
@staffCheck()
async def viewcommand(ctx, cmd_name: str):
    global maybot
    path = FCF(maybot, cmd_name)
    print(path)
    if not path:
         await ctx.send("File not Found")
         return
    content = ""
    async with aiofiles.open(path, "r", encoding='utf-8') as file:
        content = await file.read()
    content = f"```py\n{content.replace(getKG(),'(backtick)')}\n```"
    if "maybrain.py" not in path:
        if len(content) < 1950:
            await ctx.send(content)
        else:
            await ctx.send(file=File(path))
    else:
        command_code = await extract_command_code(path, cmd_name)
        content = f"```py\n{command_code.replace(getKG(),'(backtick)')}\n```"
        if len(content) < 1950:
            await ctx.send(content)
        else:
            await ctx.send(file=File(path))
    

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(viewcommand)
    return viewcommand