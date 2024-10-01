import disnake
from disnake.ext import commands
from Utilities.staffchecks import modcheck
import time
import random
import json
import os
import time



maybot = None

@commands.command(name="moditem", description="Moderation actions") # Declaration
@modcheck() # Check call to another method. Command execution will fail if this check fails
async def moditem(ctx, digit: int = None):
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
    
    if digit == None:
        await ctx.send("No ID Stated")
        return
    
    logs = load_data()
    if str(digit) in logs.keys():
        lock = 1
        data = logs[str(digit)]
        
        for i in data.keys():
            action = "".join(data[i].keys())
            dataa = data[i][action]
            embed = disnake.Embed(title=f"{i}'s {action.upper()}",description=f"{str('Length: ' + dataa['length'] + '\n') if 'length' in dataa.keys() else ''}Reason: {dataa['reason']}\nMod: {dataa['mod']}\nAction ID: {digit}")
            await ctx.send(embed=embed)
    if lock == 0:
        await ctx.send(f"{digit} ID has no modlogs")
        
            
    save_data(logs)


            
    
    
    

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(moditem)
    return moditem