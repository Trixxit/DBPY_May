from disnake.ext import commands
import disnake
from Utilities.discord_utils import create_embed
from Utilities.json_methods import read_json, write_json, maptoJSON
from Utilities.staffchecks import Anystaffcheck, admin, lcm, mod, leadeval, trainee

@commands.command(name='rolewhitelist', description="whitelist someone from custom roles", aliases=["rwl", "rwhitelist"])
@Anystaffcheck((admin, lcm, mod, leadeval, trainee))
async def rolewhitelist(ctx, mem: disnake.Member):
    try:
        data = (await read_json(maptoJSON("rolestuff.json")))
        if str(mem.id) in data["blacklisted"]:
            r = data["blacklisted"].index(str(mem.id))
            data["blacklisted"].pop(r)
            await write_json(maptoJSON("rolestuff.json"), data)
            chan = ctx.bot.get_channel(1185285161164750992)
            if chan:
                mes = await ctx.send(f"{mem.mention} has been role whitelisted!")
                embed = create_embed(description=f"Role Whitelist | {mem.display_name}", color=disnake.Colour.dark_grey(), fields=[{'name': 'User', 'value': mem.mention}, {'name': 'Moderator', 'value': ctx.author.mention}, {'name': 'Message Link', 'value': mes.jump_url}])
                await chan.send(embed=embed)
            else:
                await ctx.send("Channel not found.")
        else:
            await ctx.send(f"{mem.mention} is not blacklisted!")
    except disnake.Forbidden:
        await ctx.send("I don't have permission to do that.")

def setup_command(cog):
    cog.bot.add_command(rolewhitelist)
    rolewhitelist.extras["example"] = "No Example Set"
    return rolewhitelist