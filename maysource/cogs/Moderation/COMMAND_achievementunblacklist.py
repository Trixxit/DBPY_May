from disnake.ext import commands
import disnake

from Utilities.discord_utils import create_embed
from Utilities.staffchecks import Anystaffcheck, admin, lcm, mod, leadeval, trainee

@commands.command(name='aunblacklist', description="Unblacklist a person from the achievement system")
@Anystaffcheck((admin, lcm, mod, leadeval, trainee))
async def achievementunblacklist(ctx, mem: disnake.Member, *, reason: str = ""):
    try:
        role = ctx.guild.get_role(1194556618860400701)
        if role:
            chan = ctx.bot.get_channel(1185285161164750992)
            if chan:
                await mem.remove_roles(role)
                mes = await ctx.send(f"{mem.mention} has been unblacklisted from the achievement system!")
                embed = create_embed(description=f"Achievement Unblacklist | {mem.display_name}", color=disnake.Colour.light_grey(), fields=[{'name': 'User', 'value': mem.mention}, {'name': 'Moderator', 'value': ctx.author.mention}, {'name': 'Reason', 'value': "No reason provided" if reason == "" else reason}, {'name': 'Message Link', 'value': mes.jump_url}])
                await chan.send(embed=embed)
            else:
                await ctx.send("Channel not found.")
        else:
            await ctx.send("Role not found.")
    except disnake.Forbidden:
        await ctx.send("I don't have permission to do that.")


def setup_command(cog):
    cog.bot.add_command(achievementunblacklist)
    return achievementunblacklist