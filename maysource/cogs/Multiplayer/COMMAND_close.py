from disnake.ext import commands
import disnake
import json
import asyncio
import random




@commands.command(name="close", help="closes registrations")
@commands.cooldown(1, 10, commands.BucketType.default)
async def close(ctx, *, typed: str = "All"):
    await ctx.message.delete()



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
    guests = load_guest_data()


    if typed == "All":
        rooms = load_data()
        guests = load_guest_data()
        if int(ctx.author.id) in rooms.keys():
            embed = disnake.Embed(title=f"{ctx.author.display_name}'s room, room code `{rooms[int(ctx.author.id)]['code']}` for {rooms[int(ctx.author.id)]['region']} has been removed", description=f"# Room `{rooms[int(ctx.author.id)]['code']}` removed!")
            await ctx.send(embed=embed)
            del rooms[int(ctx.author.id)]

        if ctx.author.id in guests:
        
            embed = disnake.Embed(title=f"{ctx.author.display_name}, your guest registration has been removed")
            del guests[ctx.author.id]
            await ctx.send(embed=embed)
    

            


    
    save_data(rooms)
    save_guest_data(guests)



def setup_command(cog):
    cog.bot.add_command(close)
    return close