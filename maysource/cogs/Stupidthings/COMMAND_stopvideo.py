from disnake.ext import commands

@commands.command(name='stopvideo', description="Stops playing a video")
@commands.is_owner()
async def stopvideo(ctx):
    await ctx.voice_client.disconnect()

def setup_command(cog):
    cog.bot.add_command(stopvideo)
    return stopvideo