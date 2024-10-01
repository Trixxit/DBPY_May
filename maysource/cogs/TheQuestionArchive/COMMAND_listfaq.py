from disnake.ext import commands
from Utilities.json_methods import read_json,  maptoJSON
import disnake


class CatDropdownView(disnake.ui.View):
    def __init__(self, linked, categories):
        super().__init__()

        self.add_item(CatDropdown(linked, categories))




class CatDropdown(disnake.ui.StringSelect):
    def __init__(self, linked, categories):
        self.linked = linked
        options = [
            disnake.SelectOption(
                label=category
            ) for category in categories
        ]

        super().__init__(
            placeholder="Choose category...",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, inter: disnake.MessageInteraction):
        data = await read_json(maptoJSON("listfaq.json")) 
        keys = data["FAQ"]
        category = self.values[0]
        if category in keys:
            paragraph = f"\n[Back to top]({self.linked})\n## {category} FAQ:\n- "
            items = keys[category]
            paragraph += ", ".join(items.keys())
        else:
            await inter.response.send_message(f"The category `{category}` does not exist.", ephemeral=True)
            return 
        await inter.response.send_message(paragraph, ephemeral=True)




@commands.command(name="ListFAQ", aliases=["listq", "qlist", "faqlist"], description="Lists every information from TheQuestionArchive")
async def ListFAQ(ctx):
    data = await read_json(maptoJSON("listfaq.json")) 
    keys = data["FAQ"]
    paragraph = ""
    mesg = await ctx.send("[FAQ](https://cdn.discordapp.com/attachments/1197741765051023440/1230767745159790603/faq_e024dcf938.png?ex=66236149&is=66220fc9&hm=27c76021c42d26438ae1f6de048fe586f9f0ae3bd220abd082951cd59f43a30f&.png)")
    linked = mesg.jump_url
    categories = []
    for category in keys:
        categories.append(category)
    view = CatDropdownView(linked, categories)
    await ctx.send("Pick FAQ category:", view=view)

        

def setup_command(cog):
    cog.bot.add_command(ListFAQ)
    return ListFAQ