from disnake.ext import commands
import disnake
from Utilities.staffchecks import admincheck
from Utilities.json_methods import read_json, maptoJSON, FindkeyCIS
from Utilities.discord_utils import create_embed, randcolor

@commands.command(name='printtask', description="Sends the embed of staff tasks")
@admincheck()
async def printtasks(ctx, *, strin: str = None):
    data = await read_json(maptoJSON("tasks.json"))

    if not strin:
        embed = create_embed(title="Staff Tasks", color=randcolor())
        for category, tasks in data.items():
            task_list = '- ' + '\n- '.join(tasks.keys()) if tasks else "No tasks"
            embed.add_field(name=f"{category} Tasks", value=task_list, inline=False)
    else:
        found = False
        for category, tasks in data.items():
            result = FindkeyCIS(tasks, strin)
            if result:
                sdata = tasks[result]
                embed = create_embed(title=result, description=f"{category} Task", color=randcolor(), fields=[
                    {"name": "Description", "value": sdata["Description"]},
                    {"name": "Participants", "value": "<@" + ">, <@".join(sdata["Participants"]) + ">" if len(sdata["Participants"]) > 0 else "No Participants"},
                    {"name": "Deadline", "value": sdata["Due Date"] if sdata["Due Date"] != "-1" else "No deadline"},
                    {"name": "Notes", "value": len(sdata["Notes"]) if sdata["Notes"] else "No attached notes"}
                ])
                found = True
                break
        if not found:
            await ctx.send("Project name not found.")
            return

    await ctx.send(embed=embed)

def setup_command(cog):
    cog.bot.add_command(printtasks)
    return printtasks
