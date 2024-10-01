from disnake.ext import commands
import disnake
import json
import random

@commands.command(name="qotdsend", help="Host a multiplayer queue")
async def qotdsend(ctx):
    
    rnames = [r.name for r in ctx.author.roles]
    if "Community Manager" not in rnames and "Moderator" not in rnames:
        await ctx.send(f"No perms")
        return


    def save_data(data):
        datad = {
            i: data[i] for i in data.keys()
        }
        print(datad)

        with open("qotds.json", "w") as write_file:
            json.dump(datad, write_file)
        with open("qotds.json", "r") as read_file:
                datak = json.load(read_file)
        print(datak)
        return datad
    
    def load_data():
        try:
            with open("qotds.json", "r") as read_file:
                data = json.load(read_file)
            datad = {}
            for i in data.keys():
                datad[i] = data[i]
        except FileNotFoundError:
            datad = {"index": 52}
            save_data(datad)
        return datad
    
    qotds = load_data()
    qotds["index"] = int(qotds.get("index")) + 1
    tr = 1
    while tr == 1:
        qotdi = random.choice([i for i in qotds.keys()])
        if qotdi != "index":
            tr = 0
    qotd = qotds[qotdi]
    del qotds[qotdi]
    guildc = ctx.guild.channels
    for c in guildc:
        if "qotd" in c.name and "answers" not in c.name:
            await c.send(f"# <@&1219477051384401950> {qotds.get('index')}, {qotd}")
    
    save_data(qotds)
    


def setup_command(cog):
    cog.bot.add_command(qotdsend)
    return qotdsend