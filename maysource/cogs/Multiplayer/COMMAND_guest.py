from disnake.ext import commands
import disnake
import json
import asyncio
import random
@commands.command(name="queue", help="registers as guest")
@commands.cooldown(1, 10, commands.BucketType.default)
async def queue(ctx):

    await ctx.message.delete()
    if ctx.channel.id != 1186636726119174224:
        await ctx.send(f"Go to https://discord.com/channels/971700371112198194/1186636726119174224")
        return




    def save_data(data):
        datad = {
            int(i): data[i] for i in data.keys()
        }
        print(datad)

        with open("rooms.json", "w") as write_file:
            json.dump(datad, write_file)
        with open("rooms.json", "r") as read_file:
                datak = json.load(read_file)
        print(datak)
        return datad
    
    def load_data():
        try:
            with open("rooms.json", "r") as read_file:
                data = json.load(read_file)
            datad = {}
            for i in data.keys():
                datad[int(i)] = data[i]
        except FileNotFoundError:
            datad = {}
            save_data(datad)
        return datad
    def save_guest_data(data):
        datad = {
            int(i): data[i] for i in data.keys()
        }
        print(datad)

        with open("roomsguest.json", "w") as write_file:
            json.dump(datad, write_file)
        with open("roomsguest.json", "r") as read_file:
                datak = json.load(read_file)
        print(datak)
        return datad
    def load_guest_data():
        try:
            with open("roomsguest.json", "r") as read_file:
                data = json.load(read_file)
            datad = {}
            for i in data.keys():
                datad[int(i)] = data[i]
        except FileNotFoundError:
            datad = {}
            save_guest_data(datad)
        return datad




    rooms = load_data()
    region = None
    roles = ctx.author.roles
    def findregion(roled):
      for r in roled:
        print(r.name)
        if r.name.lower().strip() == "asia" or r.name.lower().strip() == "north america" or r.name.lower().strip() == "south america" or r.name.lower().strip() == "europe" or r.name.lower().strip() == "australia" or r.name.lower().strip() == "africa":
            region = r.name
            return region
    region = findregion(roles)
    guests = load_guest_data()
    guests[ctx.author.id] = int(ctx.author.id)
    regional = {}
    for r in rooms.keys():
        roomregion = findregion(ctx.guild.get_member(int(r)).roles)
        if roomregion == region:
            regional[r] = rooms[r]
    tr = 0
    lock = {}
    if len(regional.keys()) > 5:
        for t in range(5):
            r = list(regional.keys())
            p = random.choice(r)
            lock[p] = regional[p]
    elif len(regional.keys()) > 0:
        for t in range(len(regional.keys())):
            r = list(regional.keys())
            p = random.choice(r)
            lock[p] = regional[p]
    else:
        tr = 1

    desc = f"Available Rooms for the {region} region: \n"
    if tr == 0:
        for i in lock.keys():
            desc += f"<@{i}>'s room code: `{lock[i]['code']}`\n{lock[i]['description']}"
    
    


            


    print(regional)

            






    











    if tr == 1:
        color = disnake.Color(16711680)
    elif tr == 0:
        color = disnake.Color(65280)
    
    


    embed = disnake.Embed(title=f"{ctx.author.display_name}, you have registered as a guest", description=desc, colour=color)
    await ctx.send(embed=embed)
    save_guest_data(guests)
    save_data(rooms)
    await asyncio.sleep(3*60*60)
    if ctx.author.id in guests.keys():
        del guests[ctx.author.id]
    save_guest_data(guests)
    save_data(rooms)
    
    



def setup_command(cog):
    cog.bot.add_command(queue)
    return queue