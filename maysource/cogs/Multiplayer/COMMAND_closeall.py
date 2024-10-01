from disnake.ext import commands 
import disnake 
import json
"""
@commands.command(name="closeall", help="Closes all open rooms and guest")
async def closeall(ctx):
    rnames = [r.name for r in ctx.author.roles]
    if "Staff" not in rnames:
        await ctx.send("No perms")
        return
    """