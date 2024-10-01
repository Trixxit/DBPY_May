import disnake
from disnake.ext import commands

from Utilities.json_methods import maptoJSON, read_json, write_json
from Utilities.staffchecks import modcheck

@commands.command(name='unbind', description="Unbind a discord account from their PID")
@modcheck()
async def unbind(ctx, mem: disnake.Member):
    data = await read_json(maptoJSON("achi.json"))
    if not str(mem.id) in data["IDs"].keys():
        await ctx.send("Member not found in JSON!")
        return
    plid = data["IDs"][str(mem.id)]
    data["IDs"].pop(str(mem.id))
    await write_json(maptoJSON("achi.json"), data)
    await ctx.send(f"{mem.name} | `{mem.id}` has been unbound from PID `{plid}`")

def setup_command(cog):
    cog.bot.add_command(unbind)
    return unbind