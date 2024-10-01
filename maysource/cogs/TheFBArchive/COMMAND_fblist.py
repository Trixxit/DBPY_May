from disnake.ext import commands
from Utilities.json_methods import rmFindAlg, read_json, maptoJSON
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake


class FBDropdown(disnake.ui.StringSelect):
    def __init__(self, category, listd):
        options = listd

        super().__init__(
            placeholder=f"Choose Fatebound from {category}...",
            min_values=1,
            max_values=1,
            options=options,
        )
    async def callback(self, inter: disnake.MessageInteraction):
        data = await read_json(maptoJSON("aliases.json"))
        strub = self.values[0]
        print(strub)
        result = rmFindAlg(strub, data) 
        if result is None:
            await inter.response.send_message("Fatebound not found.")
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
            if hexeffect != "Not available":
                embed = create_embed(title=name, description=fullname if fullname else None, fields=[{"name": "Effect", "value":effect},{"name":"Hex Effect", "value": hexeffect if hexeffect else "Data Unavailable."} , {"name":"Where to Get", "value": where_to_get if where_to_get else "Data Unavailable."}], color=randcolor(), thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.0.25", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
            else:
                embed = create_embed(title=name, description=fullname if fullname else None, fields=[{"name": "Effect", "value":effect}, {"name":"Where to Get", "value": where_to_get if where_to_get else "Data Unavailable."}], color=randcolor(), thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.025", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
            await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            await inter.response.send_message("Fatebound not found...", ephemeral=True)
        

class CatDropdown(disnake.ui.StringSelect):
    def __init__(self):

        options = [
            disnake.SelectOption(
                label="Armor", description="Armor Type Fatebounds", emoji="<:SlotChest:1193935766271828161>"
            ),
            disnake.SelectOption(
                label="Stats", description="Stats Type Fatebounds", emoji="<:Health:1192950904865964052>"
            ),
            disnake.SelectOption(
                label="Offensive", description="Offensive Type Fatebounds", emoji="<:AttackPower:1192950899316903977>"
            ),
            disnake.SelectOption(
                label="Defensive", description="Defensive Type Fatebounds", emoji="<:Defense:1192951020188344501>"
            ),
            disnake.SelectOption(
                label="Utility", description="Utility Type Fatebounds", emoji="<:Cog:1179635724925030442>"
            ),
            disnake.SelectOption(
                label="Elemental", description="Elemental Type Fatebounds", emoji="<:BonusCold:1192948996931596429>"
            ),
            disnake.SelectOption(
                label="Event", description="Event Boss Type Fatebounds", emoji="<:Nian:1228609764871770152>"
            ),
            disnake.SelectOption(
                label="Premium", description="Premium Bundle Fatebound", emoji="<:fbYellow:1185706945504608367>"
            ),
            disnake.SelectOption(
                label="Mystraea", description="Mystraea Boss Type Fatebounds", emoji="<:chillsteadvillage:1221130702666338355>"
            ),
            disnake.SelectOption(
                label="Esoteria", description="Esoteria Boss Type Fatebounds", emoji="<:HumanVark:1228643553387741185>"
            ),
            disnake.SelectOption(
                label="Xandu", description="Xandu Boss Type Fatebounds", emoji="<:LumenEnclave:1199765931388321872>"
            ),
            disnake.SelectOption(
                label="NPC", description="NPC Type Fatebounds", emoji="<:May:1195000074174988439>"
            ),
            disnake.SelectOption(
                label="Insanes", description="Insanes Type Fatebounds", emoji="<:SoulCaliber:1194129109136179220>"
            ),
            disnake.SelectOption(
                label="Helhearts", description="Helhearts Type Fatebounds", emoji="<:Primo_Hellheart:1224041356301959310>"
            )
        ]

        super().__init__(
            placeholder="Choose category...",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, inter: disnake.MessageInteraction):
        data = await read_json(maptoJSON("holyarchive.json")) 
        keys = data["FateBounds"]
        category = self.values[0].capitalize()
        if category in keys:
            items = keys[category]
            listy = [i for i in items.keys()]
            view = FBDropdownView(category, listy)
            await inter.response.send_message(f"Pick Fatebound from {self.values[0]} Category:", view=view, ephemeral=True)



class CatDropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(CatDropdown())

class FBDropdownView(disnake.ui.View):
    def __init__(self, category, listy):
        super().__init__()
        self.add_item(FBDropdown(category, listy))

@commands.command(name="fblist", description="Lists every FB from the holy archive")
async def fblist(ctx):
    mesg = await ctx.send("[FAQ](https://cdn.discordapp.com/attachments/1197741765051023440/1230767745159790603/faq_e024dcf938.png?ex=66236149&is=66220fc9&hm=27c76021c42d26438ae1f6de048fe586f9f0ae3bd220abd082951cd59f43a30f&.png)")
    view = CatDropdownView()
    await ctx.send("Pick Fatebound category:", view=view)

@commands.slash_command(name="fbsearch", description="Lists every FB from the holy archive", guild_ids=[971700371112198194])
async def fbsearch(inter: disnake.ApplicationCommandInteraction, tags: str = commands.Param(default=None, description="Optional search tag for a specific Fatebounds"), query: str = commands.Param(default=None, description="Optional search term for a specific Fatebound")):
    embed = create_embed(title="Fatebound List", color=randcolor(), thumbnail_url="https://cdn.discordapp.com/attachments/1197741765051023440/1230767745159790603/faq_e024dcf938.png?ex=66236149&is=66220fc9&hm=27c76021c42d26438ae1f6de048fe586f9f0ae3bd220abd082951cd59f43a30f&.png")
    data = await read_json(maptoJSON("holyarchive.json"))
    if tags:
        names = []
        tagger = tags.split(" ")
            
        for cat in data["FateBounds"]:
            for fb in data["FateBounds"][cat].keys():
                datad = data["FateBounds"][cat][fb]
                tag = datad.get("Tags", [])
                    
                for i in tag:
                    if i in tagger:
                        print(fb)
                        names.append(fb)
            
        tagsstr = ", ".join(i for i in tagger if not i.lower().startswith("tag"))
            
        if names == []:
            embed = disnake.Embed(title=f"For tags: {tagsstr}", description=f"No results")
            await inter.send(embed=embed, ephemeral=True)
            return
        else:
            na = "\n".join(names)
            embed = disnake.Embed(title=f"For tags: {tagsstr}", description=f"{na}")
            await inter.send(embed=embed, ephemeral=True)
            return
    if query:
        strub = query
        data = await read_json(maptoJSON("holyarchive.json"))
        
        
        
        data = await read_json(maptoJSON("aliases.json"))
        print(strub)
        result = rmFindAlg(strub, data)
        print(result)
        
        if result is None:
            await inter.send("Fatebound not found.")
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
                    if secondary_data.get(i, None) != None:
                        f.append([i, secondary_data.get(i, None)])
            
            rant = randcolor()
            
            if hexeffect != "Not available":
                embed = create_embed(title=name, description=fullname if fullname else None, fields=[{"name": t[0], "value": t[1]} for t in f], color=rant, thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.0.25", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
                embed2 = create_embed(title=f"{name}'s Where to Get:", description=where_to_get, color=rant, thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.0.26", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
            else:
                embed = create_embed(title=name, description=fullname if fullname else None, fields=[{"name": t[0], "value": t[1]} for t in f], color=rant, thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.0.25", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
                embed2 = create_embed(title=f"{name}'s Where to Get:", description=where_to_get, color=rant, thumbnail_url=secondary_data["Thumbnail"], footer={"text": "version 1.2.0.26", "icon_url": "https://cdn.discordapp.com/attachments/1244715536567504906/1247900645483216977/images_13.jpg?ex=6661b58a&is=6660640a&hm=4117c289bdd36819b10d7183688d0981b04919fc4b8536bd5be8e2982ab1570e&.png"})
            
            await inter.send(embeds=[embed, embed2])
        else:
            await inter.send("Fatebound not found.")
    else:
        await inter.response.send_message(embed=embed, view=CatDropdownView(), ephemeral=True)



def setup_command(cog):
    cog.bot.add_command(fblist)
    cog.bot.add_slash_command(fbsearch)
    return fblist