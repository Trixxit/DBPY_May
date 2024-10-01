from disnake.ext import commands
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None

@commands.command(name= "EndSeason", aliases=["es", "season end", "end season", "seasonend", "endofseason"], description="Shows how many days left for the current season.")
async def EndSeason(ctx):
    embed = create_embed(title="End of Season", description="S2 will end <t:1720987200:R>, <t:1720987200:f>; and S3 will start <t:1721268000:R>, <t:1721268000:f> except for iOS devices for which the update will begin <t:1721354400:R>, <t:1721354400:f>", color=randcolor())
    await ctx.send(embed=embed)

def setup_command(cog):
    cog.bot.add_command(EndSeason)
    return EndSeason