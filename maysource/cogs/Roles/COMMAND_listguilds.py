from disnake.ext import commands
import disnake
from Utilities.staffchecks import Anystaffcheck
from Utilities.json_methods import read_json, write_json, maptoJSON
import re
from datetime import datetime, timedelta
from disnake import Embed
import json




def save_data(data = None):
    if data == None:
        data = {}
    with open("guilds.json", "w") as write_file:
        json.dump(data, write_file)
    with open("guilds.json", "r") as read_file:
        data = json.load(read_file)
    return data



def load_data():
    try:
        with open("guilds.json", "r") as read_file:
            data = json.load(read_file)
    except FileNotFoundError:
        data = save_data()
    return data
        

@commands.command(name='listguilds', description="gwah")
#@Anystaffcheck((1231831222930636800, 971704489520300032))
@commands.cooldown(1, 10, commands.BucketType.user)
async def listguilds(ctx, guildname: str = None):
    database = load_data()
    guildmembers = []
    guildnames = []
    guildnamesh = []
    if len(database.keys()) != 0:
        for g in database.keys():
            name = database[g]["Name"]
            guildnames.append(name.lower())
            guildnamesh.append(name)
            mems = database[g]["Members"]
            for m in mems:
                guildmembers.append(m)
    if (guildname != None):
        if (guildname.lower() in guildnames):
            for g in database.keys():
                name = database[g]["Name"]
                if name.lower() == guildname.lower():
                    data = database[g]
        
            embed = Embed(title=f"{data['Name']}", description=f"Member Count: {len(data['Members'])}")
        else:
            embed = Embed(title=f"Guild Name Not Found", description=f"All current guilds:\n{'\n'.join(guildnamesh)}")
    else:
        embed = Embed(title=f"Guild Name Not Specified", description=f"All current guilds:\n{'\n'.join(guildnamesh)}")
    await ctx.send(embed=embed)




    



def setup_command(cog):
    cog.bot.add_command(listguilds)
    listguilds.extras["example"] = "No Example Set"
    return listguilds