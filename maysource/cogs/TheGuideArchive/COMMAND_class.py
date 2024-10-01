from disnake.ext import commands
from Utilities.json_methods import rmFindAlg, read_json, maptoJSON
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None

@commands.command(name="Class", aliases=["c", "viewclass", "vc", "classguide"], description="View an available class guide")
async def Guide(ctx, *, strub: str):
    if strub.lower() == 'list':
        return
    data = await read_json(maptoJSON("classaliases.json"))
    print(strub)
    result = rmFindAlg(strub, data)
    print(result)
    if result is None:
        await ctx.send("Guide not found.")
        return
    data = await read_json(maptoJSON("classguide.json"))
    secondary_data = None
    name = None
    for category in data["Guide"]:
        if result in data["Guide"][category]:
            name = result
            secondary_data = data["Guide"][category][result]
            break

    if secondary_data:
        info = secondary_data.get("Info","")
        UK = secondary_data.get("Class Guide", "")
        image = secondary_data.get("Image", "Not Available")
        thumbnail = secondary_data.get("Thumbnail", "")
        emoji = secondary_data.get("Emoji", "")
        embed = create_embed(title=emoji+" "+name, description=info if info else None, fields=[{"name": "Class Guide", "value":UK if UK else "Not Yet Available!"}], footer={"text": "Kanban Musume Client Services", "icon_url": "https://cdn.discordapp.com/emojis/1228803807249432736.png"}, color=randcolor(), image_url=image, thumbnail_url=thumbnail)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Guide not found.")

def setup_command(cog):
    cog.bot.add_command(Guide)
    return Guide 