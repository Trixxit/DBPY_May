from disnake.ext import commands
from Utilities.json_methods import rmFindAlg, read_json, maptoJSON
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake




class LocationDropdown(disnake.ui.StringSelect):
    def __init__(self, linked, optionsd):
        self.linked = linked
        options = [
            disnake.SelectOption(
                label=i[0], emoji=i[1]
            ) for i in optionsd
        ]
        super().__init__(
            placeholder=f"Choose a location...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        linked = self.linked
        data = await read_json(maptoJSON("npc.json"))
        emojied = data[self.values[0]].get("Emoji", "")
        title = f"{emojied} {self.values[0]}"
        desc = f"## NPCs in {emojied} {self.values[0]}\n[Back to the top]({linked})\n\n\n"
        npcs = []
        for i in data[self.values[0]]:
            if i != "Emoji":
                d = f"{i}"
                emoji = data[self.values[0]][i].get("Emoji", "")
                npcs.append([d, emoji])
                desc += f"{emoji} {i}\n"
        desc += f"\nSelect NPC from {emojied} {self.values[0]}:"
        loc = f"{self.values[0]}"
        view = NPCDropdownView(linked, npcs, loc)
        embed = disnake.Embed(title=title, description=desc, color=randcolor())
        await inter.response.send_message(embed=embed, ephemeral=True, view=view)


class NPCDropdown(disnake.ui.StringSelect):
    def __init__(self, linked, optionsd, location):
        self.linked = linked
        self.location = location
        options = [
            disnake.SelectOption(
                label=i[0], emoji=i[1]
            ) for i in optionsd
        ]
        super().__init__(
            placeholder=f"Choose NPC from {location}...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, inter: disnake.MessageInteraction):
        linked = self.linked
        location = self.location
        data = await read_json(maptoJSON("npc.json"))
        emojied = data[location][self.values[0]].get("Emoji", "")
        desc = f"[Back to top]({linked})\n\n"
        desc += data[location][self.values[0]].get("Description", "")
        title = f"{emojied} {self.values[0]}"
        embed = disnake.Embed(title=title, description=desc, color=randcolor())
        await inter.response.send_message(embed=embed, ephemeral=True)


class NPCDropdownView(disnake.ui.View):
    def __init__(self, linked, options, location):
        super().__init__()

        self.add_item(NPCDropdown(linked, options, location))

class LocationDropdownView(disnake.ui.View):
    def __init__(self, linked, options):
        super().__init__()

        self.add_item(LocationDropdown(linked, options))





@commands.command(name="npc", description="Finds details about an NPC")
async def npc(ctx, *, stringy: str = None):
    if stringy == None:
        data = await read_json(maptoJSON("npc.json"))
        mesg = await ctx.send("[FAQ](https://cdn.discordapp.com/attachments/1197741765051023440/1230767745159790603/faq_e024dcf938.png?ex=66236149&is=66220fc9&hm=27c76021c42d26438ae1f6de048fe586f9f0ae3bd220abd082951cd59f43a30f&.png)")
        linked = mesg.jump_url
        options = []
        for i in data:
            emoji = data[i]["Emoji"]
            options.append([i, emoji])
        view = LocationDropdownView(linked, options)
        await ctx.send("Pick NPC location:", view=view)
    else:
        data = await read_json(maptoJSON("npc.json"))
        for i in data:
            for t in data[i]:
                if t.lower() == stringy.lower():
                    emojied = data[i][t].get("Emoji", "")
                    desc = f""
                    desc += data[i][t].get("Description", "")
                    title = f"{emojied} {t}"
                    embed = disnake.Embed(title=title, description=desc, color=randcolor())
                    await ctx.send(embed=embed)
                    break







def setup_command(cog):
    cog.bot.add_command(npc)
    return npc