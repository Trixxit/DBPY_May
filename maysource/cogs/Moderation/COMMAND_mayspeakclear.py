import disnake
from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import time
import random
import json
import os
import time


maybot = None


@commands.command(name="mayspeakclear", description="Norton Antivirus removes 99% of all spyware!")
@Anystaffcheck((1196761863002787971, 1256636057680609422))
async def mayspeakclear(ctx):
    def checking(t):
            return t.author == ctx.author and t.channel == ctx.channel
    code = "".join([str(random.randint(0, 9)) for i in range(0, random.randint(4, 8))])
    await ctx.send(f"Are you sure? Type in this code to confirm: `{code}`")

    confirm = await ctx.bot.wait_for('message', check=checking)
    if code == confirm.content:
        await ctx.send("Confirmed!")
    else:
        await ctx.send("Cancelled!")
        return
    maydata = {}
    with open("mayspeak.json", "w") as write_file:
            json.dump(maydata, write_file)
            


    
    
    

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(mayspeakclear)
    return mayspeakclear