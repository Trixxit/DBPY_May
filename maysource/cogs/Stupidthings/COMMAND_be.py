from disnake.ext import commands
import random, asyncio
from Utilities.staffchecks import staffCheck

maybot = None


@commands.command(name='ban_everyone', description="Joke command dw dw (Outputs total member count + General role amount)")
@staffCheck()
async def be(ctx):
    if True:
        global maybot
        def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(f"Proceeding will result in `{ctx.guild.member_count}` deaths, which will take approximately `{(random.randint(1, 100) / 10000) * ctx.guild.member_count}` seconds to execute. Are you sure you want to proceed?")
        message = await maybot.wait_for('message', check=check)
        await ctx.send(f"Executing command...\nYou may watch the progress here: <https://tools.darvin.de/info?url_short=cdn.discord.com/attachements/971700371112198194/ban_list.txt>")
    print("nuh uh")
    
def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(be)
    return be