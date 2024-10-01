from disnake.ext import commands
import disnake
import json

@commands.command(name="qotdadd", help="Host a multiplayer queue")
async def qotdadd(ctx, *, qotd: str = None):
    if qotd == None:
        await ctx.send(f"QotD is missing `>>qotdadd <qotd>`")
        return
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
    qotds["index"] = int(qotds.get("index"))

    qotds[ctx.message.id] = f"{qotd}"
    await ctx.send(f"@silent Qotd Preview: <@&1219477051384401950> {qotds.get('index')}, {qotd}")
    save_data(qotds)
    


def setup_command(cog):
    cog.bot.add_command(qotdadd)
    return qotdadd