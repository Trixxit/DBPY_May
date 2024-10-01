from disnake.ext import commands
from Utilities.json_methods import read_json, write_json, maptoJSON

@commands.command(name='bind', description="Bind your PID to your discord account! You’ll only be able to have submissions with the same PID as this verified. Note: this is an **__irreversible action__**")
async def dontcheatpls(ctx, id: int):    
    data = await read_json(maptoJSON("achi.json"))

    if str(ctx.author.id) in data["IDs"].keys():
        await ctx.send(f"You've already bound the PID `{data['IDs'][str(ctx.author.id)]}` to your account!")
        return
    
    for x, y in data["IDs"].items():
        if y == id:
            await ctx.send("This ID has already been bound to another account!")
            return
        
    data["IDs"][str(ctx.author.id)] = id
    await write_json(maptoJSON("achi.json"), data)
    await ctx.send(f"Bound `{id}` to your account! You may now submit using ``>>submit``!")

def setup_command(cog):
    cog.bot.add_command(dontcheatpls)
    return dontcheatpls