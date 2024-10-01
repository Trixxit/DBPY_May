from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import requests
import disnake

@commands.command(name="zulan", help="zulan for good")
@Anystaffcheck((1231831222930636800,1180945644567941272, 1180945644567941272))
async def zulan(ctx, *, message):
    await ctx.message.delete()
    channel = ctx.channel
    webhook = await channel.create_webhook(name='MayWebhook')
    
    

    await webhook.send(
        content=message,
        username="Zulan",
        avatar_url="https://cdn.discordapp.com/emojis/1228643549420191825.png"
    )
    await webhook.delete()


def setup_command(cog):
    cog.bot.add_command(zulan)
    zulan.extras["example"] = "No Example Set"
    return zulan