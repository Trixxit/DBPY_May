from disnake.ext import commands
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None

description = "There are three different ores in the game."
lydite = "Upgrades the level of an equipment to the player’s current level. If the equipment is level 30 or above and challenging difficulty is unlocked, it can be upgraded to M tier. If the equipment is level 50 and heroic difficulty is unlocked, it can be upgraded to G tier. If the equipment is level 60 and heroic is unlocked, it can be upgraded to S tier."
weathered = "Used to reroll secondary Fatebounds. You cannot reroll primary Fatebounds or special Fatebounds (spirit of x, insane equipment specials, etc). You can reroll secondary Fatebounds using a forging statue as well — a rare statue found in dungeons."
volcanic = "Used to reroll primary (ones that come with the equipment) modifiers on an equipment. You can also reroll primary modifiers using a forging statue — a rare statue found in dungeons."

@commands.command(name= "Ores", aliases=["ore", "lydite", "weatheredhephaestite", "volcanichephaestite", "volcanic", "weathered"], description="View information regarding ores.")
async def Ores(ctx):
    embed = create_embed(title="Ores", description=description, fields=[{"name": "<:Lydite:1187175260462792775>Lydite", "value":lydite},{"name": "<:WeatheredHephaestite:1187175247015850065>Weathered Hephaestite", "value": weathered}, {"name": "<:VolcanicHephaestite:1187175264082468964>Volcanic Hephaestite", "value": volcanic}], color=randcolor())
    await ctx.send(embed=embed)

def setup_command(cog):
    cog.bot.add_command(Ores)
    return Ores