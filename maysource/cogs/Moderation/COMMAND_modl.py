import disnake
from disnake.ext import commands
from Utilities.staffchecks import modcheck
import time
import random
import json
import os
import time



maybot = None

@commands.command(name="modlogs", description="Moderation actions") # Declaration
@modcheck() # Check call to another method. Command execution will fail if this check fails
async def modlogs(ctx, user: disnake.Member = None):
    def save_data(data):
        datad = {
            int(i): data[i] for i in data.keys()
        }
        print(datad)

        with open("mod.json", "w") as write_file:
            json.dump(datad, write_file)
        with open("mod.json", "r") as read_file:
                datak = json.load(read_file)
        print(datak)
        return datad
    
    def load_data():
        try:
            with open("mod.json", "r") as read_file:
                data = json.load(read_file)
            datad = {}
            for i in data.keys():
                datad[i] = data[i]
        except FileNotFoundError:
            datad = {}
            save_data(datad)
        return datad
    
    if user == None:
        await ctx.send("No Member Stated")
        return
    print(user.id)
    logs = load_data()
    lock = 0
    for i in logs.keys():
        lock = 1
        data = logs[i]
        
        if str(user.id) in data.keys():
            action = "".join(data[str(user.id)].keys())
            dataa = data[str(user.id)][action]
            embed = disnake.Embed(title=f"{user.display_name}'s {action.upper()}",description=f"{str('Length: ' + dataa['length'] + '\n') if 'length' in dataa.keys() else ''}Reason: {dataa['reason']}\nMod: {dataa['mod']}\nAction ID: {i}")
            await ctx.send(embed=embed)
    if lock == 0:
        await ctx.send(f"{user.mention} has no modlogs")
        
            
    save_data(logs)


            
    
    # written with discord
    

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(modlogs)
    return modlogs