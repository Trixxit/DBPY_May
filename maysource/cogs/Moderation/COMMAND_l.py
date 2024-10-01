from disnake.ext import commands
import random, asyncio, json
import disnake
from Utilities.staffchecks import staffCheck

maybot = None


@commands.command(name='l', description="Language servers", aliases=["server", "servers"])
async def l(ctx, *, langu: str = None):
    
    def save_data(data):
        datad = {
            int(i): data[i] for i in data.keys()
        }
        print(datad)

        with open("langs.json", "w") as write_file:
            json.dump(datad, write_file)
        with open("langs.json", "r") as read_file:
                datak = json.load(read_file)
        print(datak)
        return datad
    
    def load_data():
        try:
            with open("langs.json", "r") as read_file:
                data = json.load(read_file)
            datad = {}
            for i in data.keys():
                datad[i] = data[i]
        except FileNotFoundError:
            datad = {}
            save_data(datad)
        return datad
    langsu = load_data()
    if langu == None:
        txt = ""
        for i in langsu.keys():
            datat = langsu[i]
            lang = datat.get("lang")
            link = datat.get("link")
            desc = datat.get("desc")
            txt += f"{lang}: {i}\n"
        embed = disnake.Embed(title="Language not stated", description=f"Listing available connected servers: \n{txt}")
        await ctx.send(embed=embed)
        return
    if langu in langsu.keys():
        datat = langsu[langu]
        lang = datat.get("lang")
        link = datat.get("link")
        desc = datat.get("desc")
        embed = disnake.Embed(title=f"{lang} Server", description=f"Server Invite Link: {link}\nRule 8: {desc}")
        await ctx.send(f"{link}", embed=embed)
    else:
        await ctx.send("Language not found")
    
def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(l)
    return l