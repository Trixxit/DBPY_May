from disnake.ext import commands
import disnake
import asyncio
from Utilities.staffchecks import Anystaffcheck, admin, leadeval, mod, headguide, lcm, trainee

@commands.command(name='FMWR', description="Finds all users with the inputted role")
@Anystaffcheck((admin, leadeval, mod, headguide, lcm, trainee))
async def rolepeek(ctx, role: disnake.Role):
    members_with_role = [member for member in ctx.guild.members if role in member.roles]
    members_with_role.sort(key=lambda m: m.display_name.lower())
    max_members_per_page = 30
    pages = [members_with_role[i:i + max_members_per_page] for i in range(0, len(members_with_role), max_members_per_page)]
    current_page = 0

    def create_embed_for_page(page_index):
        embed = disnake.Embed(title=f"Members with {role.name}", color=role.color)
        member_mentions = "\n".join(member.mention for member in pages[page_index])
        embed.add_field(name="Members", value=member_mentions, inline=False)
        embed.set_footer(text=f"Page {page_index+1} of {len(pages)}")
        return embed

    if not pages:
        await ctx.send("No members found with this role.")
        return

    message = await ctx.send(embed=create_embed_for_page(current_page))

    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["⬅️", "➡️"]

    while True:
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == "➡️" and current_page < len(pages) - 1:
                current_page += 1
                await message.edit(embed=create_embed_for_page(current_page))
            elif str(reaction.emoji) == "⬅️" and current_page > 0:
                current_page -= 1
                await message.edit(embed=create_embed_for_page(current_page))

            await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.clear_reactions()
            break

def setup_command(cog):
    cog.bot.add_command(rolepeek)
    return rolepeek
