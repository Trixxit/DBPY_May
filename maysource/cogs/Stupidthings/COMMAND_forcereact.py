from disnake.ext import commands
import disnake
import re

from Utilities.staffchecks import Anystaffcheck, admin, leadeval

@commands.command(name='forcereact', description="Forces may to react to a message")
@Anystaffcheck((admin, leadeval, 1231831222930636800))
async def forcereact(ctx, message_link: str, emoji: str):
    # Parse the message link
    match = re.search(r'discord\.com/channels/(\d+)/(\d+)/(\d+)', message_link)
    if not match:
        await ctx.send("Invalid message link.")
        return

    _, channel_id, message_id = map(int, match.groups())

    channel = ctx.bot.get_channel(channel_id)
    if not channel:
        await ctx.send("Channel not found.")
        return

    try:
        message = await channel.fetch_message(message_id)
    except disnake.NotFound:
        await ctx.send("Message not found.")
        return
    except disnake.Forbidden:
        await ctx.send("I don't have permission to access that message.")
        return
    except disnake.HTTPException:
        await ctx.send("Failed to retrieve the message.")
        return
    try:
        await message.add_reaction(emoji)
        await ctx.send("Reaction added.")
    except disnake.HTTPException:
        await ctx.send("Failed to add the reaction.")


def setup_command(cog):
    cog.bot.add_command(forcereact)
    return forcereact