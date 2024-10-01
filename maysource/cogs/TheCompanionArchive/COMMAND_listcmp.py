from disnake.ext import commands
from Utilities.json_methods import read_json,  maptoJSON

@commands.command(name="ListCompanions", aliases=["listpet", "listanimal", "cmplist", "petlist"], description="Lists every Companion from the holy archive")
async def listcmp(ctx, *, cat: str = None):
    data = await read_json(maptoJSON("PetInfo.json")) 
    keys = data["Companions"]
    paragraph = ""
    await ctx.send("[FAQ](https://cdn.discordapp.com/attachments/1197741765051023440/1230767745159790603/faq_e024dcf938.png?ex=66236149&is=66220fc9&hm=27c76021c42d26438ae1f6de048fe586f9f0ae3bd220abd082951cd59f43a30f&.png)")

    if cat is None:  
        parapgraph = "# Companions"
        for category in keys:
            paragraph += f"\n{category}\n-# • "  
            items = keys[category]
            paragraph += ", ".join(items.keys())
            print(paragraph)
            await ctx.send(paragraph)
            paragraph = ""
    else:
        category = cat.capitalize()
        if category in keys:
            paragraph += f"\n {category} Companion:\n-# • "
            items = keys[category]
            paragraph += ", ".join(items.keys())
        else:
            await ctx.send(f"The category `{cat}` does not exist.")
            return 
        await ctx.send(paragraph)


def setup_command(cog):
    cog.bot.add_command(listcmp)
    return listcmp