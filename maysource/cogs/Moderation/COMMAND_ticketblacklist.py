from disnake.ext import commands
import disnake
from Utilities.discord_utils import create_embed

from Utilities.staffchecks import modle

@commands.command(name='tblacklist', description="Blacklist a person from the ticket system", aliases=["ticketblacklist", "tickblacklist", "tbl"])
@modle()
async def ticketblacklist(ctx, mem: disnake.Member, *, reason: str = ""):
    global maybot
    try:
        role = ctx.guild.get_role(1185184698767523850)
        if role:
            chan = ctx.bot.get_channel(1185285161164750992)
            if chan:
                await mem.add_roles(role)
                mes = await ctx.send(f"{mem.mention} has been ticket blacklisted!")
                embed = create_embed(description=f"Ticket Blacklist | {mem.display_name}", color=disnake.Colour.dark_grey(), fields=[{'name': 'User', 'value': mem.mention}, {'name': 'Moderator', 'value': ctx.author.mention}, {'name': 'Reason', 'value': "No reason provided" if reason == "" else reason}, {'name': 'Message Link', 'value': mes.jump_url}])
                await chan.send(embed=embed)
            else:
                await ctx.send("Channel not found.")
        else:
            await ctx.send("Role not found.")
    except disnake.Forbidden:
        await ctx.send("I don't have permission to do that.")

def setup_command(cog):
    cog.bot.add_command(ticketblacklist)
    return ticketblacklist