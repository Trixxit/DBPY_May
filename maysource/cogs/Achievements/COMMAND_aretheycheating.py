from disnake.ext import commands
import disnake
from Utilities.json_methods import maptoJSON, read_json
from Utilities.staffchecks import user_has_role
from Utilities.staffchecks import modevalcheck

@commands.command(name='checkid', description="Checks the bound PID of an inputted member", aliases=["pid", "checkpid", "id"])
@modevalcheck()
async def aretheycheating(ctx, mem):
    
    data = await read_json(maptoJSON("achi.json"))
    t = mem
    mem = ""
    for i in t:
        if i.isdigit():
            mem += i

    
    for b in data["IDs"].keys():
        if str(mem) == str(data["IDs"][b]):
            await ctx.send(f"The member <@{b}> | `{b}` has the PID `{mem}` bound!")
            return
        elif str(mem) in data["IDs"].keys():
            await ctx.send(f"The member <@{mem}> | `{mem}` has the PID `{data['IDs'][str(mem)]}` bound!")
            return
    
    await ctx.send(f"The specified member with id `{mem}` has no bound PID!")
    

def setup_command(cog):
    cog.bot.add_command(aretheycheating)
    return aretheycheating