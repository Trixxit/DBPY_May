from disnake.ext import commands
import disnake
from Utilities.discord_utils import create_embed
from Utilities.staffchecks import modcheck
from fuzzywuzzy import fuzz


@commands.command(name='SFM', description="No, this does not stand for SatisFactory Modding.")
@modcheck()
async def ScarlixFamilyMembers(ctx, *, search: str):
    close_matches = []
    threshold = 90 

    for member in ctx.guild.members:
        nickname = member.nick if member.nick else member.name 
        similarity = fuzz.partial_ratio(search.lower(), nickname.lower())
        if similarity >= threshold:
            close_matches.append(f"{member.mention} ({similarity}%)")

    if close_matches:
        response = "- " + "\n- ".join(close_matches)
    else:
        response = "No close matches found."

    embed = create_embed(title=f"{search} Members", description=response)
    await ctx.send(embed=embed)


def setup_command(cog):
    cog.bot.add_command(ScarlixFamilyMembers)
    return ScarlixFamilyMembers