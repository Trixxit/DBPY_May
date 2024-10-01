from disnake.ext import commands
import disnake
from Utilities.staffchecks import all_staff, staffguideCheck
from Utilities.roles import bases
import asyncio

@commands.command(name='liststaff', description="Lists all staff and their roles")
@staffguideCheck()
async def ListStaff(ctx, highest_only: bool = False):
    roles = [ctx.guild.get_role(x) for x in all_staff if ctx.guild.get_role(x)]
    chunkamount = 20
    if not roles:
        await ctx.send("No staff roles found.")
        return

    embeds = []

    special_role = ctx.guild.get_role(1180235184747057162)

    for role in roles:
        if role == special_role and not highest_only:
            special_members = []
            for member in ctx.guild.members:
                if special_role in member.roles:
                    base_roles = [ctx.guild.get_role(base_id).name for base_id in bases if ctx.guild.get_role(base_id) in member.roles]
                    member_desc = f"- {member.mention} ({', '.join(base_roles) if base_roles else 'No class selected'})"
                    special_members.append(member_desc)

            chunks = [special_members[i:i + chunkamount] for i in range(0, len(special_members), chunkamount)]
            for chunk in chunks:
                embed = disnake.Embed(title=f"{role.name} - Staff List", description="\n".join(chunk) if chunk else "No members with this role.", color=disnake.Color.blurple())
                embeds.append(embed)
        else:
            members_with_role = [f"- {member.mention}" for member in ctx.guild.members if role in member.roles]
            chunks = [members_with_role[i:i + chunkamount] for i in range(0, len(members_with_role), chunkamount)]
            for chunk in chunks:
                embed = disnake.Embed(title=f"{role.name} - Staff List", description="\n".join(chunk) if chunk else "No members with this role.", color=disnake.Color.blurple())
                embeds.append(embed)

    if not embeds:
        await ctx.send("No staff members found.")
        return

    message = await ctx.send(embed=embeds[0])
    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

    index = 0

    while True:
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == "➡️" and index < len(embeds) - 1:
                index += 1
                await message.edit(embed=embeds[index])
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "⬅️" and index > 0:
                index -= 1
                await message.edit(embed=embeds[index])
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break
    await message.clear_reactions()

def setup_command(cog):
    cog.bot.add_command(ListStaff)
    return ListStaff
