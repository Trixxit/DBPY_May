import disnake
from disnake.ext import commands
from Utilities.staffchecks import modcheck
import time
import random
import json
import os
import time



maybot = None

@commands.command(name="bakspeak", description="Mod speak") 
@modcheck() 
async def bakspeak(ctx, *, message: str = None):
    if message != None:
        await ctx.message.delete()
        channel = ctx.channel
        webhook = await channel.create_webhook(name='MayWebhook')
    
    

        await webhook.send(
            content=message,
            username="Black Archknight",
            avatar_url="https://cdn.discordapp.com/attachments/1179551792959328297/1263315240242905098/dak.png?ex=6699c980&is=66987800&hm=0b40da486d0fffaf7873069af6e0aab3b925f2f9b90512a19a4d10947d4aa2b5&"
        )
        await webhook.delete()

            
    
    
    

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(bakspeak)
    return bakspeak