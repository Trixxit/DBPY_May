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
        



@commands.command(name='createguild', description="gwah")
@Anystaffcheck((1231831222930636800, 1183701097857163384))
@commands.cooldown(1, 10, commands.BucketType.user)
async def createguild(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    database = load_data()
    guildmembers = []
    guildnames = []
    if len(database.keys()) != 0:
        for g in database.keys():
            name = database[g]["Name"]
            guildnames.append(name)
            mems = database[g]["Members"]
            for m in mems:
                guildmembers.append(m)
    if str(ctx.author.id) in database.keys():
        data = database[str(ctx.author.id)]
        guildname = data.get("Name", "No Name Found")
        await ctx.send(f"<@{ctx.author.id}>, you cannot make another guild, you already own {guildname}")
    elif str(ctx.author.id) in guildmembers:
        for g in database.keys():
            mems = database[g]["Members"]
            if str(ctx.author.id) in mems:
                data = database[g]
                guildname = data.get("Name", "No Name Found")
                await ctx.send(f"<@{ctx.author.id}>, you cannot make another guild, you are already in {guildname}")
    else:
        await ctx.send("Please enter the name for the guild: ")
        namemsg = await ctx.bot.wait_for('message', check=check)
        name = namemsg.content
        while name in guildnames:
            await ctx.send("Name already in use!\nPlease enter the name for the guild: ")
            namemsg = await ctx.bot.wait_for('message', check=check)
            name = namemsg.content
        database[str(ctx.author.id)] = {
            "Name": name,
            "Members":[str(ctx.author.id)]
        }
        mems = database[str(ctx.author.id)]["Members"]
        embed = Embed(title=f"Guild {name} has been created!", description=f"<@{ctx.author.id}> has made guild {name} with {len(mems)} member")
        await ctx.send(embed=embed)
    save_data(database)




    



def setup_command(cog):
    cog.bot.add_command(createguild)
    createguild.extras["example"] = "No Example Set"
    return createguild