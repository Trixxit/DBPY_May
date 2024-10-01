from disnake.ext import commands

@commands.command(name='muteall', description="Mutes all people who have spoken in the context chat for an hour")
async def purgechat(ctx):
    print("Blank command")

def setup_command(cog):
    cog.bot.add_command(purgechat)
    return purgechat