from disnake.ext import commands
from Utilities.json_methods import rmFindAlg, read_json, maptoJSON
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None

@commands.command(name="Companion", aliases=["cmp", "pet", "animal"], description="View a documented companion")
async def CMP(ctx, *, strub: str):    
    data = await read_json(maptoJSON("PetInfo.json"))
    secondary_data = None
    name = None
    print(strub)
    for category in data["Companions"]:
        for key in data["Companions"][category]:
            print(key)
            if key.lower() == strub.lower():
                name = key
                secondary_data = data["Companions"][category][key]
                break
            elif strub.lower() in data["Companions"][category][key]["Aliases"]:
                name = key
                secondary_data = data["Companions"][category][key]
                break


    if secondary_data:
        f = []
        for k in secondary_data.keys():
            if k != "Emoji" and k != "Thumbnail" and k != "Aliases":
                if secondary_data.get(k, "") != "":
                    f.append([k, secondary_data.get(k, "")])
        thumbnail = secondary_data.get("Thumbnail", "")
        em = secondary_data.get("Emoji", "")
        embed = create_embed(title=em+" "+name, fields=[{"name":t[0], "value":t[1]} for t in f], color=randcolor(), thumbnail_url=thumbnail)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Companion not found.")



def setup_command(cog):
    cog.bot.add_command(CMP)
    return CMP
