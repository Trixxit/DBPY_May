from disnake.ext import commands
from Utilities.staffchecks import staffguideCheck
from Utilities.json_methods import read_json, maptoJSON, rmFindAlg

@commands.command(name="listaliases", aliases=["listalias", "aliases", "la"], description="Sends every alias attached to a fate bound")
async def la(ctx, *, fatebound: str):
    data = await read_json(maptoJSON("aliases.json"))
    fatebound = fatebound.lower()
    print(fatebound)
    result = rmFindAlg(fatebound, data) 
    print(result)
    if result is None:
        await ctx.send("Fatebound not found.")
        return
    else:
        await ctx.send(f"``{result}``'s aliases are: {', '.join(data[result])}")

def setup_command(cog):
    cog.bot.add_command(la)
    return la