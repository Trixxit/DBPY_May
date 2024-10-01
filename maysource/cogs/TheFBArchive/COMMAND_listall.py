from disnake.ext import commands
from Utilities.staffchecks import staffguideCheck
import disnake
from Utilities.json_methods import maptoJSON, read_json

@commands.command(name='listall')
async def listall(ctx, category: str):
    archive_data = (await read_json(maptoJSON("holyarchive.json")))["FateBounds"]
    alias_data = await read_json(maptoJSON("aliases.json"))
    if category not in archive_data:
        await ctx.send(f"Category '{category}' not found.")
        return
    fatebounds = archive_data[category]

    embed = disnake.Embed(title=f"Aliases in Category '{category}'", color=disnake.Color.blue())

    for fatebound, details in fatebounds.items():
        aliases = alias_data.get(fatebound, [])
        alias_list = ', '.join(aliases) if aliases else 'No aliases found'
        embed.add_field(name=fatebound, value=alias_list, inline=False)
    await ctx.send(embed=embed)

def setup_command(cog):
    cog.bot.add_command(listall)
    return listall