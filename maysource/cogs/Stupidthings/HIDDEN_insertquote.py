from disnake.ext import commands
from Utilities.json_methods import read_json, write_json, maptoJSON
from Utilities.staffchecks import Anystaffcheck, admin, lcm, mod, cm
import disnake

@commands.command(name='insertdquote', description="Insert a member quote for the `dquote` command", aliases=["addquote", "aq", "idq", "quotethis"])
@Anystaffcheck((admin, lcm, mod, cm, 1180945644567941272, 1196465778438963392))
async def insertdquote(ctx, *, stri = None):
    if stri is None and ctx.message.reference:
        ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        stri = "'" + ref_message.content + "' - " + ref_message.author.display_name

    if stri:
        stri = stri.replace("'", "")
        stri = f"'{stri}'"
        data = await read_json(maptoJSON("stuff.json"))
        data["Quotes"].append(stri)
        await write_json(maptoJSON("stuff.json"), data)
        await ctx.send("Quote successfully added!")
    else:
        await ctx.send("No quote provided!")

def setup_command(cog):
    cog.bot.add_command(insertdquote)
    insertdquote.extras["example"] = "No Example Set"
    return insertdquote