import disnake
from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import time
import random
import json
import os
import time


maybot = None



@commands.command(name="mayspeak", description="We're in your walls...")
@Anystaffcheck((1196761863002787971, 1256636057680609422))
async def mayspeak(ctx, sending: disnake.TextChannel = None, listening: disnake.TextChannel = None):
    if not sending:
        nuhuh = [
            "Nuh uh! You didn't put a channel to receive the messages",
            "You bum! You did not put in the correct stuff!",
            "*bonk* You forgot something!",
            "*sigh* You just can't do anything without my help, can you?"
        ]
        await ctx.send(random.choice(nuhuh), reference=ctx.message)
        return
    if not listening:
        listening = ctx.channel
    
    with open("mayspeak.json", "r") as read_file:
                maydata = json.load(read_file)

    locks = [i for i in maydata.keys()]

    def checking(t):
            return t.author == ctx.author and t.channel == ctx.channel
    if len(locks) >= 1:
        code = "".join([str(random.randint(0, 9)) for i in range(0, random.randint(4, 8))])
        await ctx.send(f"Are you sure? Type in this code to confirm: `{code}`")
        confirm = await ctx.bot.wait_for('message', check=checking)
        if code == confirm.content:
            await ctx.send("Confirmed!")
        else:
            await ctx.send("Cancelled!")
            return
    
    maydata[str(listening.id)] = str(sending.id)


    with open("mayspeak.json", "w") as write_file:
            json.dump(maydata, write_file)
    
    


            


    
    
    

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(mayspeak)
    return mayspeak