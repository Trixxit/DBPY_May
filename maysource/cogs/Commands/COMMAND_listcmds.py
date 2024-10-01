from disnake.ext import commands
from Utilities.staffchecks import staffguideCheck

maybot = None

@commands.command(name='listcmds')
@staffguideCheck()
async def listcmds(ctx):
    global maybot
    total = "```md\nCOGS:"
    for cog_name, cog in sorted(maybot.cogs.items()):
        total += f"\n Cog: {cog_name}"

    # Handling commands not associated with any cog
    no_cog_commands = [cmd for cmd in maybot.commands if not cmd.cog]
    if no_cog_commands:
        total += "\n\n Commands:"
        for command in sorted(no_cog_commands, key=lambda x: x.name):
            aliases = ', '.join([command.name] + command.aliases)
            total += f"\n- Command IN: {command.callback.__name__}, Triggers/Aliases: {aliases}"

    total += "\n```"
    await ctx.send(total)


def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(listcmds)
    return listcmds