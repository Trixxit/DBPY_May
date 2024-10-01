from disnake.ext import commands

from Utilities.json_methods import maptoJSON, read_json

@commands.command(name='mypid', description="Check your bound PID")
async def mypid(ctx):
    data = await read_json(maptoJSON("achi.json"))
    if str(ctx.author.id) not in data["IDs"].keys():
        await ctx.send("You don't have an associated PID!")
        return
    await ctx.send(f"{ctx.author.mention}, your PID is `{data['IDs'][str(ctx.author.id)]}`")

def setup_command(cog):
    cog.bot.add_command(mypid)
    return mypid