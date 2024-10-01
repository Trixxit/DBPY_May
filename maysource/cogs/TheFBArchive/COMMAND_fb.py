from disnake.ext import commands
from Utilities.json_methods import rmFindAlg, read_json, maptoJSON
from Utilities.discord_utils import create_embed, randcolor
# from Utilities.staffchecks import staffguideCheck
import random
import disnake

maybot = None

@commands.command(name="fb", aliases=["fatebound", "viewfb", "vfb"], description="view a logged fatebound")
@commands.cooldown(1, 3, commands.BucketType.default)
# @staffguideCheck()
async def vfb(ctx, *, strub: str):
    
    data = await read_json(maptoJSON("holyarchive.json"))
    if strub.lower() == 'list':
        return
    if strub.lower().startswith("tag"):
        names = []
        tagger = strub.split(" ")
        for cat in data["FateBounds"]:
            for fb in data["FateBounds"][cat].keys():
                datad = data["FateBounds"][cat][fb]
                tags = datad.get("Tags", [])
                for i in tags:
                  if i in strub.split(" "):
                    print(fb)
                    names.append(fb)
        tagsstr = ", ".join(i for i in tagger if not i.lower().startswith("tag"))
        if names == []:

            embed = disnake.Embed(title=f"For tags: {tagsstr}", description=f"No results")
            await ctx.send(embed=embed)
            return
        
        else:
            na = "\n".join(names)
            
            embed = disnake.Embed(title=f"For tags: {tagsstr}", description=f"{na}")
            await ctx.send(embed=embed)
            return
    data = await read_json(maptoJSON("aliases.json"))
    print(strub)
    result = rmFindAlg(strub, data) 
    print(result)
    if result is None:
        await ctx.send("Fatebound not found.")
        return
    data = await read_json(maptoJSON("holyarchive.json"))
    secondary_data = None
    name = None
    for category in data["FateBounds"]:
        if result in data["FateBounds"][category]:
            name = result
            secondary_data = data["FateBounds"][category][result]
            break

    if secondary_data:
        effect = secondary_data.get("Effect", "Not available")
        where_to_get = secondary_data.get("Where To Get", "Not available")
        hexeffect = secondary_data.get("Helxar-Touched Effect", "Not available")
        fullname = secondary_data.get("Fullname", "")
        f = []
        for i in secondary_data.keys():
            if i != "Fullname" and i != "Where To Get" and i != "Thumbnail" and i != "Tags" and i != "ID":
                if secondary_data.get(i,None) != None:
                    f.append([i, secondary_data.get(i,None)])
        rant = randcolor()
        if hexeffect != "Not available":
            embed = create_embed(title=name, description=fullname if fullname else None, fields=[{"name": t[0], "value":t[1]} for t in f], color=rant, thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.0.25", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
            embed2 = create_embed(title=f"{name}'s Where to Get:", description=where_to_get, color=rant, thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.0.26", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
        else:
            embed = create_embed(title=name, description=fullname if fullname else None, fields=[{"name": t[0], "value":t[1]} for t in f], color=rant, thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.0.25", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
            embed2 = create_embed(title=f"{name}'s Where to Get:", description=where_to_get, color=rant, thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.0.26", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
        await ctx.send(embeds=[embed, embed2])
    else:
        await ctx.send("Fatebound not found.")



def setup_command(cog):
    cog.bot.add_command(vfb)
    return vfb