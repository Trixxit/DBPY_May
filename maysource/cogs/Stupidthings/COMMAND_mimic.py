from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import requests
import disnake

@commands.command(name="mimic", help="mimic for good")
@Anystaffcheck((1231831222930636800,1180945644567941272, 1180945644567941272))
async def mimic(ctx, user: disnake.Member, *, message):
    await ctx.message.delete()
    channel = ctx.channel
    webhook = await channel.create_webhook(name='MayWebhook')
    print(ctx.author.display_name)
    print(user)
    user_display_name = user.nick
    print(user.nick)
    avatar_urled = user.guild_avatar
    if avatar_urled != None:
        avatar_urled = user.guild_avatar.url
    else:
        avatar_urled = user.avatar.url
    print(avatar_urled)
    if user.nick == None:
        user_display_name = user.display_name

    await webhook.send(
        content=message,
        username=user_display_name,
        avatar_url=avatar_urled
    )
    await webhook.delete()


def setup_command(cog):
    cog.bot.add_command(mimic)
    mimic.extras["example"] = "No Example Set"
    return mimic