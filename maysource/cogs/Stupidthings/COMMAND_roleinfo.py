import disnake
from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck, lcm, leadguide, leadeval

@commands.command(name="roleinfo")
@Anystaffcheck((lcm, leadguide, leadeval))
async def roleinfo(ctx, *, role_identifier: str):
    try:
        role_id = int(role_identifier)
        role = ctx.guild.get_role(role_id)
    except ValueError:
        role = disnake.utils.get(ctx.guild.roles, name=role_identifier)

    if not role:
        await ctx.send("Role not found!")
        return

    embed = disnake.Embed(title=f"Role Information: {role.name}", color=role.color)
    embed.add_field(name="Role ID", value=role.id, inline=True)
    embed.add_field(name="Members", value=len(role.members), inline=True)
    embed.add_field(name="Color", value=str(role.color), inline=True)

    if role.icon:
        embed.set_thumbnail(url=role.icon.url)
        embed.add_field(name="Icon URL", value=role.icon.url, inline=False)
    else:
        embed.add_field(name="Icon URL", value="No icon", inline=False)

    embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
    embed.add_field(name="Position", value=role.position, inline=True)
    embed.add_field(name="Created At", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

    await ctx.send(embed=embed)
    
def setup_command(cog):
    cog.bot.add_command(roleinfo)
    return roleinfo