from disnake.ext import commands
import disnake
from Utilities.staffchecks import admincheck
from Utilities.json_methods import read_json, write_json, maptoJSON, FindkeyCIS
import asyncio
import re

@commands.command(name='edittask', description="Edit tasks in the tasks list")
@admincheck()
async def edittasks(ctx, *, task_name: str):
    data = await read_json(maptoJSON("tasks.json"))

    task_found = False
    for category, tasks in data.items():
        for task in tasks:
            if task.lower() == task_name.lower():
                task_found = True
                task_data = tasks[task]
                break
        if task_found:
            break

    if not task_found:
        await ctx.send("Task not found.")
        return

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel


    await ctx.send("Do you want to change the task name? (yes/no)")
    try:
        response = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        if response.content.lower() == 'yes':
            await ctx.send("Enter the new task name:")
            new_name = await ctx.bot.wait_for('message', check=check, timeout=60.0)
            data[category][new_name.content] = data[category].pop(task)
            task = new_name.content
            task_data = data[category][task]
    except asyncio.TimeoutError:
        await ctx.send("Timed out. Continuing with other edits.")

    await ctx.send("Do you want to change the description? (yes/no)")
    try:
        response = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        if response.content.lower() == 'yes':
            await ctx.send("Enter the new description:")
            new_description = await ctx.bot.wait_for('message', check=check, timeout=60.0)
            task_data["Description"] = new_description.content[:1000]
    except asyncio.TimeoutError:
        await ctx.send("Timed out. Continuing with other edits.")

    # Edit Deadline
    await ctx.send("Do you want to change the deadline? (yes/no)")
    try:
        response = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        if response.content.lower() == 'yes':
            await ctx.send("Enter the new deadline:")
            new_deadline = await ctx.bot.wait_for('message', check=check, timeout=60.0)
            task_data["Due Date"] = new_deadline.content
    except asyncio.TimeoutError:
        await ctx.send("Timed out. Continuing with other edits.")

    # Edit Participants
    await ctx.send("Do you want to add or remove participants? (add/remove/both/none)")
    try:
        response = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        if response.content.lower() in ['add', 'both']:
            await ctx.send("Enter the IDs or mentions of participants to add (separated by space):")
            new_participants = await ctx.bot.wait_for('message', check=check, timeout=60.0)
            participant_ids_to_add = re.findall(r'(\d{17,20})', new_participants.content)
            task_data["Participants"].extend(participant_ids_to_add)
            task_data["Participants"] = list(set(task_data["Participants"])) 

        if response.content.lower() in ['remove', 'both']:
            await ctx.send("Enter the IDs or mentions of participants to remove (separated by space):")
            participants_to_remove = await ctx.bot.wait_for('message', check=check, timeout=60.0)
            participant_ids_to_remove = re.findall(r'(\d{17,20})', participants_to_remove.content)
            task_data["Participants"] = [p for p in task_data["Participants"] if p not in participant_ids_to_remove]
    except asyncio.TimeoutError:
        await ctx.send("Timed out. Continuing with other edits.")

    await write_json(maptoJSON("tasks.json"), data)
    await ctx.send(f"Task '{task_name}' in category '{category}' has been updated.")

def setup_command(cog):
    cog.bot.add_command(edittasks)
    return edittasks
