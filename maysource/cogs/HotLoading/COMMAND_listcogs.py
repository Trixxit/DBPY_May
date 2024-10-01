from disnake.ext import commands
from Utilities.staffchecks import staffCheck

maybot = None

@commands.command(name='listcogs')
@staffCheck()
async def list_cogs(ctx):
    global maybot
    loaded_cogs = ', '.join(maybot.cogs.keys())
    await ctx.send(f"Loaded cogs: {loaded_cogs}")
    await ctx.send("*These are internal names, you must reload directories, not internals*")

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(list_cogs)
    return list_cogs
