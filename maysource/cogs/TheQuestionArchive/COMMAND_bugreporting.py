from disnake.ext import commands
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None

@commands.command(name= "Bug", aliases=["bugreport", "bugs", "bugsreport", "bugreports", "report"], description="View info ragarding bug report.")
async def Bug(ctx):
    embed = create_embed(title="Bug Report", description="Staff and Moderators of this Discord Server can't help you with your in game concerns. You can post your bug report at <#1169171096793251900> or email it at `info@chillyroom.games` with this format:", fields=[{"name": "1.(State which game if sending it to email.)", "value": "\n"}, {"name": "2.Description of the bug.", "value": "\n"}, {"name": "3.Device model & Operating system.", "value": "\n"}, {"name": "4.Account ID/Player ID", "value": "\n"}, {"name": "5. Add screenshot or record the bug encountered.", "value": "\n"}], color=randcolor())
    await ctx.send(embed=embed)

def setup_command(cog):
    cog.bot.add_command(Bug)
    return Bug