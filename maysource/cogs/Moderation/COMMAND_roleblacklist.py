from disnake.ext import commands
import disnake
from Utilities.discord_utils import create_embed
from Utilities.json_methods import read_json, write_json, maptoJSON
from Utilities.staffchecks import Anystaffcheck, admin, lcm, mod, leadeval, trainee

@commands.command(name='roleblacklist', description="blacklist someone from custom roles (will remove their role from existence)", aliases=["rbl", "rblacklist"])
@Anystaffcheck((admin, lcm, mod, leadeval, trainee))
async def roleblacklist(ctx, mem: disnake.Member, *, reason: str = ""):
    try:
        data = (await read_json(maptoJSON("rolestuff.json")))
        if str(mem.id) in data["blacklisted"]:
            await ctx.send(f"{mem.mention} is already blacklisted!")
            return
        else:
            data["blacklisted"].append(str(mem.id))
            await write_json(maptoJSON("rolestuff.json"), data)
            if str(mem.id) in data["customrolestuff"]:
                md = data["customrolestuff"][str(mem.id)]
                role = ctx.guild.get_role(md["id"])
                if role:
                    await role.delete()
                else:
                    await ctx.send("Failed to parse role object, so it may still exist. Continuing with blacklist.")
                data["customrolestuff"].pop(str(mem.id))
            chan = ctx.bot.get_channel(1185285161164750992)
            if chan:
                mes = await ctx.send(f"{mem.mention} has been role blacklisted!")
                embed = create_embed(description=f"Role Blacklist | {mem.display_name}", color=disnake.Colour.dark_grey(), fields=[{'name': 'User', 'value': mem.mention}, {'name': 'Moderator', 'value': ctx.author.mention}, {'name': 'Reason', 'value': "No reason provided" if reason == "" else reason}, {'name': 'Message Link', 'value': mes.jump_url}])
                await chan.send(embed=embed)
            else:
                await ctx.send("Channel not found.")
    except disnake.Forbidden:
        await ctx.send("I don't have permission to do that.")

def setup_command(cog):
    cog.bot.add_command(roleblacklist)
    roleblacklist.extras["example"] = "No Example Set"
    return roleblacklist