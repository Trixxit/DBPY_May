from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
from Utilities.json_methods import read_json, maptoJSON, rmFindAlg, write_json

@commands.command(name="removealiases", aliases=["removealias", "ra", "ralias"], description="Unlink an alias from a fatebound key")
@Anystaffcheck((1231831222930636800, 1180945644567941272))
async def ra(ctx, fatebound: str, aliastoremove: str):
    data = await read_json(maptoJSON("aliases.json"))
    fatebound = fatebound.lower()
    print(fatebound)
    result = rmFindAlg(fatebound, data) 
    print(result)
    if result is None:
        await ctx.send(f"Fatebound `{fatebound}` not found.")
        return
    else:
        if aliastoremove.lower() in data[result]:
            data[result].remove(aliastoremove.lower())
            await write_json(maptoJSON("aliases.json"), data)
            await ctx.send(f"Removed `{aliastoremove}` from `{result}`'s aliases!")
        else:
            await ctx.send(f"`{aliastoremove}` was not apart of `{result}`'s aliases...")

def setup_command(cog):
    cog.bot.add_command(ra)
    return ra