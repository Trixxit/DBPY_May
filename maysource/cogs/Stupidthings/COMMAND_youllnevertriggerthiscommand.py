from disnake.ext import commands

def buh():
    async def predicate(ctx):
        raise commands.CheckFailure("You do not have the required staff role to use this command.")
    return commands.check(predicate)


@commands.command(name='failperms', description="Command to test failing perms")
@buh()
async def youllnevertriggerthiscommand(ctx):
    print("Blank command")


def setup_command(cog):
    cog.bot.add_command(youllnevertriggerthiscommand)
    return youllnevertriggerthiscommand