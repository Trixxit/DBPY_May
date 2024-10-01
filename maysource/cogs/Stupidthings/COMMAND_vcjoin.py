from disnake.ext import commands

@commands.command(name='joinmyvc', description="Joins the trigger's vc")
@commands.is_owner()
async def vcjoin(ctx):
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel.")
        return

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(voice_channel)
    else:
        await voice_channel.connect()

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

def setup_command(cog):
    cog.bot.add_command(vcjoin)
    return vcjoin