from disnake.ext import commands
from Utilities.json_methods import rmFindAlg, read_json, maptoJSON
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None

@commands.command(name="Question", aliases=["q", "faq"], description="View info regarding faq")
async def Question(ctx, *, strub: str):
    data = await read_json(maptoJSON("qaliases.json"))
    print(strub)
    result = rmFindAlg(strub, data) 
    print(result)
    if result is None:
        await ctx.send("FAQ not found.")
        return
    data = await read_json(maptoJSON("listfaq.json"))
    secondary_data = None
    name = None
    print(strub)
    for category in data["FAQ"]:
        if result in data["FAQ"][category]:
            name = result
            secondary_data = data["FAQ"][category][result]
            break

    if secondary_data:
        UK = secondary_data.get("Description", "")
        Imgs = secondary_data.get("Imgs","")
        embeder = []
        if Imgs != None:
            for keyed in Imgs:
                print(keyed)
                embed = disnake.Embed(title=name, description=UK, color=randcolor(), url=ctx.channel.jump_url)
                embed.set_image(url=Imgs[keyed])
                embeder.append(embed)
            await ctx.send(embeds=embeder)
        else:
            print(secondary_data, "No image")
    else:
        await ctx.send("FAQ not found.")

def setup_command(cog):
    cog.bot.add_command(Question)
    return Question 
