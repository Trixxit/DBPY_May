from disnake.ext import commands
import disnake
import re
from Utilities.staffchecks import admincheck
from Utilities.json_methods import read_json, write_json, maptoJSON

@commands.command(name='addtask', description="Adds a task to the specified category")
@admincheck()
async def addtasks(ctx, category: str, task_name: str, description: str, due_date: str, *, participants_str: str):
    data = await read_json(maptoJSON("tasks.json"))

    participant_ids = re.findall(r'(\d{17,20})', participants_str)
    unique_participant_ids = list(set(participant_ids))

    task_data = {
        "Description": description,
        "Participants": unique_participant_ids,
        "Due Date": due_date,
        "Notes": []
    }

    data[category][task_name] = task_data
    await write_json(maptoJSON("tasks.json"), data)

    await ctx.send(f"Task '{task_name}' added to category '{category}' with participants: {', '.join(unique_participant_ids)}.")

def setup_command(cog):
    cog.bot.add_command(addtasks)
    return addtasks
