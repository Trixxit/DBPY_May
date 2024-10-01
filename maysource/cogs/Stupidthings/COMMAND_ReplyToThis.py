from disnake.ext import commands

@commands.command(name='rtt', description="rtt")
@commands.is_owner()
async def ReplyToThis(ctx, *, message: str):
    if ctx.message.reference is not None:
        original_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if original_msg:
            await original_msg.reply(message)
        else:
            await ctx.send("The original message could not be found.")
    else:
        await ctx.send("This command needs to be a reply to another message.")


def setup_command(cog):
    cog.bot.add_command(ReplyToThis)
    ReplyToThis.extras["example"] = "No Example Set"
    return ReplyToThis