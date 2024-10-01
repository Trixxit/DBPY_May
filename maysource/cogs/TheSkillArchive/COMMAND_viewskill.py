from disnake.ext import commands
from Utilities.json_methods import rmFindAlg, read_json, maptoJSON
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None


class BaseClassDropdown(disnake.ui.StringSelect):
    def __init__(self, base_classes):
        self.base_classes = base_classes
        self.poopy = [i[0] for i in base_classes]
        options = [disnake.SelectOption(label=t[0], emoji=t[1]) for t in base_classes]
        super().__init__(
            placeholder="Choose base class...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        data = await read_json(maptoJSON("skill.json"))
        para = f"# {self.base_classes[self.poopy.index(self.values[0])][1]} {self.values[0]} Base Class Skills:\n"
        keys = data["Primary Skills"]
        category = self.values[0]
        for key in keys[category]:
            if key == "Skills":
                for skill in keys[category][key]:
                    print(skill)
                    secondary_data = keys[category][key][skill]
                    if secondary_data:
                        para += f'## {skill} {secondary_data.get("Emoji", "")}\n'
                    else:
                        para += f"## {skill} data not found"

        if category in keys:
            items = keys[category]
            subclassesname = items["Subclasses"]
        skilled = []
        for skill in keys[category]["Skills"]:
            secondary_data = keys[category][key][skill]
            emoji = secondary_data.get("Emoji", "")
            skillp = [skill, emoji]
            skilled.append(skillp)
        keys = data["Subclasses"]
        subclasses = []
        print(subclassesname)
        for subclasseee in subclassesname:
            emoji = keys[subclasseee].get("Emoji", "")
            subclasses.append([subclasseee, emoji])
        view = SkillSubClassDropdownView(category, skilled, subclasses)
        await inter.response.send_message(
            f"{para}\nSkills and Combined Classes", ephemeral=True, view=view
        )


class SkillDropdown(disnake.ui.StringSelect):
    def __init__(self, classed, skills):
        self.classed = classed
        options = [disnake.SelectOption(label=i[0], emoji=i[1]) for i in skills]
        super().__init__(
            placeholder=f"Choose {classed} skill...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        data = await read_json(maptoJSON("skill.json"))
        keys = data["Primary Skills"]
        secondary_data = keys[self.classed]["Skills"][self.values[0]]
        title = f'{self.values[0]} {secondary_data.get("Emoji", "<:Cog:1179635724925030442>")}'
        f = []
        for k in secondary_data.keys():
            if k != "Emoji" and k != "Aliases":
                f.append([k, secondary_data.get(f"{k}", "Not available")])
        embed = create_embed(
            title=self.classed + " " + title,
            fields=[
                {"name": t[0], "value": t[1]} for t in f
            ],
            color=randcolor(),
        )
        await inter.response.send_message(embed=embed, ephemeral=True)


class SubkillDropdown(disnake.ui.StringSelect):
    def __init__(self, classed, skills):
        self.classed = classed
        options = [disnake.SelectOption(label=i[0], emoji=i[1]) for i in skills]
        super().__init__(
            placeholder=f"Choose {classed} skill...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        data = await read_json(maptoJSON("skill.json"))
        keys = data["Subclasses"]
        secondary_data = keys[self.classed]["Subskills"][self.values[0]]
        title = f'{self.values[0]} {secondary_data.get("Emoji", "<:Cog:1179635724925030442>")}'
        f = []
        for k in secondary_data.keys():
            if k != "Emoji" and k != "Aliases":
                f.append([k, secondary_data.get(f"{k}", "Not available")])
        embed = create_embed(
            title=self.classed + " " + title,
            fields=[
                {"name": t[0], "value": t[1]} for t in f
            ],
            color=randcolor(),
        )
        await inter.response.send_message(embed=embed, ephemeral=True)


class SubClassDropdown(disnake.ui.StringSelect):
    def __init__(self, classed, subclasses):
        self.subclasses = subclasses
        self.poopy = [i[0] for i in subclasses]
        self.classed = classed
        options = [disnake.SelectOption(label=i[0], emoji=i[1]) for i in subclasses]
        super().__init__(
            placeholder="Choose combined class...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        data = await read_json(maptoJSON("skill.json"))
        keys = data["Subclasses"]
        para = f"# {self.subclasses[self.poopy.index(self.values[0])][1]} {self.values[0]} Combined Class Skills:\n"
        subskills = []
        skillsk = []
        category = self.values[0]
        for key in keys[category]:
            if key == "Subskills":
                for skill in keys[category][key]:
                    print(skill)
                    secondary_data = keys[category][key][skill]
                    if secondary_data:
                        para += f'## {skill} {secondary_data.get("Emoji", "")}\n'
                        subskills.append([skill, secondary_data.get("Emoji", "<:Cog:1179635724925030442>")])
                    else:
                        para += f"## {skill} data not found"
        subclassesed = keys[category]["Base Classes"]
        keys = data["Primary Skills"]
        print(subclassesed)
        subclassesed.remove(self.classed)
        print(subclassesed)
        for cass in subclassesed:
            emoji = keys[cass].get("Emoji", "")
            para += f"# Other Base Class {emoji} {cass} Skills:\n"
            for key in keys[subclassesed[0]]:
                if key == "Skills":
                    for skill in keys[subclassesed[0]][key]:
                        print(skill)
                        secondary_data = keys[subclassesed[0]][key][skill]
                        if secondary_data:
                            para += f'## {skill} {secondary_data.get("Emoji", "<:Cog:1179635724925030442>")}\n'
                            skillsk.append([skill, secondary_data.get("Emoji", "<:Cog:1179635724925030442>")])
                        else:
                            para += f"## {skill} data not found"

        view = SubSkills(
            subclassesed[0], self.values[0], skillsk, subskills
        )
        await inter.response.send_message(
            f"{para}\nCombined Class and Other Base Class Skills",
            ephemeral=True,
            view=view,
        )


class SubSkills(disnake.ui.View):
    def __init__(self, classed, subclass, skills, subskills):
        super().__init__()
        self.add_item(SkillDropdown(classed, skills))
        self.add_item(SubkillDropdown(subclass, subskills))


class SkillSubClassDropdownView(disnake.ui.View):
    def __init__(self, classed, skills, subclasses):
        super().__init__()
        self.add_item(SkillDropdown(classed, skills))
        self.add_item(SubClassDropdown(classed, subclasses))
        


class BaseClassDropdownView(disnake.ui.View):
    def __init__(self, linked):
        super().__init__()

        self.add_item(BaseClassDropdown(linked))



@commands.command(
    name="skill",
    aliases=["vs", "viewskill", "vsk"],
    description="View a documented skill",
)
async def viewskill(ctx, * , stringy: str = None):
    if stringy == None:
        data = await read_json(maptoJSON("skill.json"))
        base_classes = []
        for c in data["Primary Skills"]:
            secondary_data = data["Primary Skills"][c]
            base_classes.append([c, secondary_data.get("Emoji", "<:Cog:1179635724925030442>")])
        print(base_classes)
        view = BaseClassDropdownView(base_classes)
        await ctx.send("Pick Base Class: (All data is limited and from S1 only for now)", view=view)
    else:
        stringyd = stringy
        stringy = ""
        for c in stringyd:
            if c != " " and c.isalpha():
                stringy += c
        data = await read_json(maptoJSON("skill.json"))
        secondary_data = None
        name = None
        for category in data["Primary Skills"]:
            for key in data["Primary Skills"][category]["Skills"]:
                print(key)
                keyd = key
                keyt = ""
                for c in keyd:
                    if c != " " and c.isalpha():
                        keyt += c
                aliasd = []
                for a in data["Primary Skills"][category]["Skills"][key]["Aliases"]:
                    t = ""
                    for ac in a:
                        if ac != " " and ac.isalpha():
                            t += ac
                    aliasd.append(t)
                if keyt.lower() == stringy.lower():
                    name = key
                    secondary_data = data["Primary Skills"][category]["Skills"][key]
                    break
                elif stringy.lower() in aliasd:
                    name = key
                    secondary_data = data["Primary Skills"][category]["Skills"][key]
                    break

        for category in data["Subclasses"]:
            for key in data["Subclasses"][category]["Subskills"]:
                print(key)
                keyd = key
                keyt = ""
                for c in keyd:
                    if c != " " and c.isalpha():
                        keyt += c
                aliasd = []
                for a in data["Subclasses"][category]["Subskills"][key]["Aliases"]:
                    t = ""
                    for ac in a:
                        if ac != " " and ac.isalpha():
                            t += ac
                    aliasd.append(t)
                if keyt.lower() == stringy.lower():
                    name = key
                    secondary_data = data["Subclasses"][category]["Subskills"][key]
                    break
                elif stringy.lower() in aliasd:
                    name = key
                    secondary_data = data["Subclasses"][category]["Subskills"][key]
                    break

        if secondary_data:
            em = secondary_data.get(f"Emoji", "<:Cog:1179635724925030442>")
            f = []
            for k in secondary_data.keys():
                if k != "Emoji" and k != "Aliases":
                    if secondary_data.get(f"{k}", "Not available") != "Not available":
                        f.append([k, secondary_data.get(f"{k}", "Not available")])
            embed = create_embed(
                title=em + " " + name,
                fields=[
                    {"name": t[0], "value": t[1]} for t in f
                ],
                color=randcolor(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Skill not found.")


    


def setup_command(cog):
    cog.bot.add_command(viewskill)
    return viewskill
