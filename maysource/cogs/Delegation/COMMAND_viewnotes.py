from disnake.ext import commands

@commands.command(name='viewnotes', description="View current notes for admin")
async def viewnotes(ctx):
    print("Blank command")

def setup_command(cog):
    cog.bot.add_command(viewnotes)
    return viewnotes