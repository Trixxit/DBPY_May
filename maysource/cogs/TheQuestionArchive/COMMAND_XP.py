from disnake.ext import commands
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None

@commands.command(name= "XP", description="Information regarding discord server XP")
async def XP(ctx):
    embed = create_embed(title="Discord Server XP", description="Image permission is provided through XP roles. To post media, you must be at least a Veteran Adventurer, given at 5000 xp. XP is given at a random amount between 20-50 xp, which is earned **per minute of chatting** —- you can check your rank in <#1105759325806411796> with `t!rank`. <#972442301760684082>, <#1186653355158810684>, & <#975586078880858132> has universal media permission.", color=randcolor())
    await ctx.send(embed=embed)

def setup_command(cog):
    cog.bot.add_command(XP)
    return XP