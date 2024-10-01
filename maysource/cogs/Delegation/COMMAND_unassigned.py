from disnake.ext import commands
from Utilities.staffchecks import admincheck, all_staff
from Utilities.json_methods import read_json, maptoJSON
from Utilities.discord_utils import create_embed

@commands.command(name='checkparticipants', description="Checks if members with certain roles are participants in tasks")
@admincheck()
async def checkparticipants(ctx):
    data = await read_json(maptoJSON("tasks.json"))
    role_set = set(all_staff)

    members_with_roles = [member for member in ctx.guild.members if set(role.id for role in member.roles) & role_set]

    all_participants = set()
    for category, tasks in data.items():
        for task in tasks.values():
            all_participants.update(task['Participants'])

    members_not_in_tasks = [member for member in members_with_roles if str(member.id) not in all_participants]

    if members_not_in_tasks:
        member_mentions = ", ".join(member.mention for member in members_not_in_tasks)
        await ctx.send(embed=create_embed(title="These members are not assigned to a project or task", description=member_mentions))
    else:
        await ctx.send("All members with the specified roles are participants in at least one task.")


def setup_command(cog):
    cog.bot.add_command(checkparticipants)
    return checkparticipants
