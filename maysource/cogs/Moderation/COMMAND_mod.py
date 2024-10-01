import disnake
from disnake.ext import commands
from Utilities.staffchecks import modcheck
import time
import random
import json
import os
import time



maybot = None

@commands.command(name="mod", description="Moderation actions") # Declaration
@modcheck() # Check call to another method. Command execution will fail if this check fails
async def mod(ctx, user: disnake.Member = None, *, things: str = None):
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
    if things == None:
        await ctx.send("No Actions Stated")
        return
    logs = load_data()
    thingsl = things.split(" ")
    tools = ["+mute", "+unmute", "+ban", "+warn"]
    for i in thingsl:
        if i == "+mute":
            start = things.find(i)
            if start != -1:
                thingscut = things[start + len(i):]
                thingscutl = thingscut.split(" ")
                
                def thingscheck(thingscutl):

                    for t in thingscutl:
                        if t in tools:
                            thingscut = " ".join(thingscutl[:thingscutl.index(t)])
                            return thingscut
                    thingscut = " ".join(thingscutl)
                    return thingscut
                thingscut = thingscheck(thingscutl)
                
                        
                
                idata = thingscut.split(" ")
                timei = idata[1].rfind("s")
                timemul = 1
                if timei == -1:
                    timei = idata[1].rfind("m")
                    timemul = 60
                if timei == -1:
                    timei = idata[1].rfind("h")
                    timemul = 60 * 60
                if timei == -1:
                    timei = idata[1].rfind("d")
                    timemul = 60 * 60 * 24
                if timei == -1:
                    await ctx.send(f"Invalid time {idata[1]}")
                    return
                print(idata[1][:timei])
                reasonl = []
                for i in range(2, len(idata)):
                    reasonl.append(idata[i])
                reason = " ".join(reasonl)
                print(reason)
                if reason.strip() == "":
                    reason = "No reason provided"
                

                sec = int(idata[1][:timei]) * timemul
                ided = random.randint(0,99999999999)
                embed = disnake.Embed(title=f"Muting {user.display_name}...", description=f"Muting {user.mention} for {idata[1][:timei+1]}\nReason: {reason}\nModerator: {ctx.author.mention}\nMod ID: {ided}")
                await ctx.send(embed=embed)
                await user.timeout(duration=sec,reason=reason)
                await ctx.bot.get_channel(1185285161164750992).send(embed=embed)
                logs[str(ided)]= {str(user.id):{"mute":{
                    "length":f"{idata[1][:timei+1]}",
                    "reason":f"{reason}",
                    "mod":f"{ctx.author.mention}"
                }}}
                



                
        elif i == "+ban":
            start = things.find(i)
            if start != -1:
                thingscut = things[start + len(i):]
                thingscutl = thingscut.split(" ")
                
                def thingscheck(thingscutl):

                    for t in thingscutl:
                        if t in tools:
                            thingscut = " ".join(thingscutl[:thingscutl.index(t)])
                            return thingscut
                    thingscut = " ".join(thingscutl)
                    return thingscut
                thingscut = thingscheck(thingscutl)
                
                        
                
                idata = thingscut.split(" ")
                timei = idata[1].rfind("s")
                timemul = 1
                if timei == -1:
                    timei = idata[1].rfind("m")
                    timemul = 60
                if timei == -1:
                    timei = idata[1].rfind("h")
                    timemul = 60 * 60
                if timei == -1:
                    timei = idata[1].rfind("d")
                    timemul = 60 * 60 * 24
                if timei == -1:
                    await ctx.send(f"Invalid time {idata[1]}")
                    return
                print(idata[1][:timei])
                reasonl = []
                for i in range(2, len(idata)):
                    reasonl.append(idata[i])
                reason = " ".join(reasonl)
                print(reason)
                if reason.strip() == "":
                    reason = "No reason provided"
                

                sec = int(idata[1][:timei]) * timemul
                ided = random.randint(0,99999999999)
                embed = disnake.Embed(title=f"Banning {user.display_name}...", description=f"Banning {user.mention}  \nDeleting {idata[1][:timei+1]} of messages\nReason: {reason}\nModerator: {ctx.author.mention}\nMod ID: {ided}")
                await ctx.send(embed=embed)
                await user.send(embed=embed)
                await user.ban(clean_history_duration=sec,reason=reason)
                await ctx.bot.get_channel(1185285161164750992).send(embed=embed)
                logs[str(ided)]= {str(user.id):{"ban":{
                    "length":f"{idata[1][:timei+1]}",
                    "reason":f"{reason}",
                    "mod":f"{ctx.author.mention}"
                }}}
                embed = disnake.Embed(title=f"{user.display_name} Ban Case", description=f"{user.mention}, you have been banned from Soulknight Prequel\nReason: {reason}")
                
        elif i == "+unmute":
            start = things.find(i)
            if start != -1:
                thingscut = things[start + len(i):]
                thingscutl = thingscut.split(" ")
                
                def thingscheck(thingscutl):

                    for t in thingscutl:
                        if t in tools:
                            thingscut = " ".join(thingscutl[:thingscutl.index(t)])
                            return thingscut
                    thingscut = " ".join(thingscutl)
                    return thingscut
                thingscut = thingscheck(thingscutl)
                
                        
                
                idata = thingscut.split(" ")
                
                reasonl = []
                for i in range(1, len(idata)):
                    reasonl.append(idata[i])
                reason = " ".join(reasonl)
                print(reason)
                if reason.strip() == "":
                    reason = "No reason provided"
                

                ided = random.randint(0,99999999999)
                embed = disnake.Embed(title=f"Unmuting {user.display_name}...", description=f"Unmuting {user.mention}\nReason: {reason}\nModerator: {ctx.author.mention}\nMod ID: {ided}")
                await ctx.send(embed=embed)
                await user.timeout(duration=None,reason=reason)
                await ctx.bot.get_channel(1185285161164750992).send(embed=embed)
                logs[str(ided)]= {str(user.id):{"unmute":{
                    "reason":f"{reason}",
                    "mod":f"{ctx.author.mention}"
                }}}
        elif i == "+warn":
            start = things.find(i)
            if start != -1:
                thingscut = things[start + len(i):]
                thingscutl = thingscut.split(" ")
                
                def thingscheck(thingscutl):

                    for t in thingscutl:
                        if t in tools:
                            thingscut = " ".join(thingscutl[:thingscutl.index(t)])
                            return thingscut
                    thingscut = " ".join(thingscutl)
                    return thingscut
                thingscut = thingscheck(thingscutl)
                
                        
                
                idata = thingscut.split(" ")
                
                reasonl = []
                for i in range(1, len(idata)):
                    reasonl.append(idata[i])
                reason = " ".join(reasonl)
                print(reason)
                if reason.strip() == "":
                    reason = "No reason provided"
                

                ided = random.randint(0,99999999999)
                embed = disnake.Embed(title=f"Warning {user.display_name}...", description=f"Warning {user.mention} for {reason}\nModerator: {ctx.author.mention}\nMod ID: {ided}")
                await ctx.send(embed=embed)
                await ctx.bot.get_channel(1185285161164750992).send(embed=embed)
                embed = disnake.Embed(title=f"Warning...", description=f"{reason}")
                await user.send(embed=embed)
                logs[str(ided)]= {str(user.id):{"warn":{
                    "reason":f"{reason}",
                    "mod":f"{ctx.author.mention}"
                }}}
        
            
        save_data(logs)


            
    
    
    

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(mod)
    return mod