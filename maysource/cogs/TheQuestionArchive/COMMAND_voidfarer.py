from disnake.ext import commands
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None

@commands.command(name= "Voidfarer", aliases=["vf", "void", "voidfarter", "voidfart"], description="Obtain Method of Voidfarer.")
async def Voidfarer(ctx):
    embed = create_embed(title="<:voidfarer:1230826392854462495>Voidfarer", description="Is obtainable through the <:s2medallion:1230829619951964160>S2 Gold Medallion, purchased with 360<:zFishChip:1187175256595644446>. At the end of the season, it will become unlockable via 500<:zGem:1187175259179339776>.", color=randcolor())
    await ctx.send(embed=embed)
    
def setup_command(cog):
    cog.bot.add_command(Voidfarer)
    return Voidfarer