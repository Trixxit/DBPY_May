from disnake.ext import commands
from Utilities.json_methods import read_json, maptoJSON, write_json, rmFindAlg
from Utilities.staffchecks import staffguideCheck

@commands.command("addfb", description="[CMD IN DEV] Add an FB to the holy archive")
@staffguideCheck()
async def afb(ctx, *, args: str):
    args = args.split('"')
    # !addfb "Armour" "Heavy Armour" "When attacked, deal 3" "On any heavy armour piece" "ha, hi, ho"
    print(args)
    '''
    category = category.lower()
    data = await read_json(maptoJSON("aliases.json"))
    result = rmFindAlg(name.lower(), data)
    if result:
        await ctx.send(f"A fatebound with the name `{name}` already exists!")
        return
    data = await read_json(maptoJSON("holyarchive.json"))
    if not any(category == key.lower() for key in data):
        await ctx.send(f"The category `{category}` does not exist.")
        return
    data[category][name] = { "Effect": effect}
    '''
        
    

def setup_command(cog):
    cog.bot.add_command(afb)
    return afb
