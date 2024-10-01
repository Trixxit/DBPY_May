from disnake.ext import commands
import disnake
from Utilities.staffchecks import Anystaffcheck
from Utilities.json_methods import read_json, maptoJSON, write_json, rmFindAlg

@commands.command(name="aa", aliases=["addalias", "adda"], description="Add an alias to a fate bound!")
@Anystaffcheck((1231831222930636800, 1180945644567941272))
async def aa(ctx, fatebound: str, *, newalias: str):
    data = await read_json(maptoJSON("aliases.json"))
    fatebound = fatebound.lower()
    print(fatebound)
    result = rmFindAlg(fatebound, data) 
    print(result)
    if result is None:
        await ctx.send(f"Fatebound `{fatebound}` not found.")
        return
    else:
        data[result].append(newalias.lower())
        await write_json(maptoJSON("aliases.json"), data)
        await ctx.send(f"Added `{newalias}` to the aliases for `{result}`")

@commands.slash_command(name="aa", description="Add an alias to a Fatebound!", guild_ids=[971700371112198194])
@Anystaffcheck((1231831222930636800, 1180945644567941272))
async def add_alias(inter: disnake.ApplicationCommandInteraction, fatebound: str = commands.Param(description="Fatebound to add the alias to"), newalias: str = commands.Param(description="New alias to add to the fatebound")):
    data = await read_json(maptoJSON("aliases.json"))
    fatebound = fatebound.lower()
    print(fatebound)
    result = rmFindAlg(fatebound, data)
    print(result)
    
    if result is None:
        await inter.response.send_message(f"Fatebound `{fatebound}` not found.", ephemeral=True)
        return
    else:
        data[result].append(newalias.lower())
        await write_json(maptoJSON("aliases.json"), data)
        await inter.response.send_message(f"Added `{newalias}` to the aliases for `{result}`", ephemeral=True)



def setup_command(cog):
    cog.bot.add_command(aa)
    cog.bot.add_slash_command(add_alias)
    return aa