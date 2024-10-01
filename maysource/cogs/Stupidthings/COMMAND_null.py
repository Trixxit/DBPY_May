from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import requests
import disnake

@commands.command(name="null", help="null for good")
@Anystaffcheck((1231831222930636800,1180945644567941272, 1180945644567941272))
async def null(ctx, *, message):
    await ctx.message.delete()
    channel = ctx.channel
    webhook = await channel.create_webhook(name='MayWebhook')
    
    

    await webhook.send(
        content=message,
        username="NULL",
        avatar_url="https://cdn.discordapp.com/attachments/972061720208105514/1246638087182880788/null_found.png?ex=665d1db1&is=665bcc31&hm=cb1f57fd38001abdecd9bfed5365c1437c610f4fedc3a6c12b9e5e4c98a86510&"
    )
    await webhook.delete()


def setup_command(cog):
    cog.bot.add_command(null)
    null.extras["example"] = "No Example Set"
    return null