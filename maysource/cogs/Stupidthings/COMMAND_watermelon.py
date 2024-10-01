from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import requests
import disnake

@commands.command(name="watermeloncat", help="watermeloncat for good")
@Anystaffcheck((1231831222930636800,1180945644567941272, 1180945644567941272))
async def watermeloncat(ctx, *, message):
    await ctx.message.delete()
    channel = ctx.channel
    webhook = await channel.create_webhook(name='MayWebhook')
    
    

    await webhook.send(
        content=message,
        username="Watermelon Cat",
        avatar_url="https://cdn.discordapp.com/emojis/1244720970711699608.png"
    )
    await webhook.delete()


def setup_command(cog):
    cog.bot.add_command(watermeloncat)
    watermeloncat.extras["example"] = "No Example Set"
    return watermeloncat