from disnake.ext import commands
from Utilities.staffchecks import admincheck
from Utilities.json_methods import read_json, write_json, maptoJSON, FindkeyCIS

@commands.command(name='deletetask', description="Delete a task from the tasks list")
@admincheck()
async def deletetask(ctx, *, task_name: str):
    data = await read_json(maptoJSON("tasks.json"))

    for category in data:
        task_key = FindkeyCIS(data[category], task_name)
        if task_key:
            del data[category][task_key]
            await write_json(maptoJSON("tasks.json"), data)
            await ctx.send(f"Task '{task_key}' has been deleted from category '{category}'.")
            return
    await ctx.send(f"Task '{task_name}' not found.")

def setup_command(cog):
    cog.bot.add_command(deletetask)
    return deletetask
