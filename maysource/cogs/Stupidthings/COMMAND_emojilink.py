from disnake.ext import commands
import disnake
from Utilities.staffchecks import staffguideCheck

@commands.command()
@staffguideCheck()
async def emojilink(ctx, emoji: disnake.PartialEmoji, size: int = 64):
    if emoji.is_custom_emoji():
        size = max(min(4096, size), 16)
        url = f"https://cdn.discordapp.com/emojis/{emoji.id}.png?size={size}"
        await ctx.send(url)
    else:
        await ctx.send("Standard emojis don't have an attachment link.")


def setup_command(cog):
    cog.bot.add_command(emojilink)
    return emojilink