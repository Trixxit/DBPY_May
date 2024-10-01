from disnake.ext import commands
import disnake
import asyncio
from Utilities.discord_utils import create_embed


LEFT_ARROW = "⬅️"
RIGHT_ARROW = "➡️"
REACTION_TIMEOUT = 60

async def paginate_commands(ctx, commands_list, page_size=10):
    pages = [commands_list[i:i + page_size] for i in range(0, len(commands_list), page_size)]
    current_page = 0

    def create_page_embed(current_page, pages):
        embed = disnake.Embed(
            title="HELP PAGE | ALL COMMANDS",
            description="Literally every command. Use `>>help (cmd)` for details.",
            color=disnake.Color.red()
        )
        page_content = "- " + '\n- '.join(pages[current_page])
        embed.add_field(name=f"Commands - Page {current_page + 1}/{len(pages)}", value=page_content)
        return embed

    message = await ctx.send(embed=create_page_embed(current_page, pages))
    await asyncio.sleep(0.5)
    await message.add_reaction(LEFT_ARROW)
    await asyncio.sleep(0.5)
    await message.add_reaction(RIGHT_ARROW)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [LEFT_ARROW, RIGHT_ARROW]

    while True:
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=REACTION_TIMEOUT, check=check)
            if str(reaction.emoji) == LEFT_ARROW and current_page > 0:
                current_page -= 1
            elif str(reaction.emoji) == RIGHT_ARROW and current_page < len(pages) - 1:
                current_page += 1

            await message.edit(embed=create_page_embed(current_page, pages))
            await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.clear_reactions()
            break

@commands.command(name='help', description="Shows the help command")
async def help(ctx, spec: str = "all"):
    global maybot
    values = []
    embed = None
    if spec == "all":
        for cog_name, cog in maybot.cogs.items():
            desc = getattr(cog, 'desc', 'No description available')
            values.append(f"{cog_name}: {desc}")
        valuestr = "- " + "\n- ".join(values)
        embed = create_embed(title="HELP PAGE | COG Categories", description="These are the categories of commands. Use `>>help (cog)` for details.", color=disnake.Color.green(), fields=[{"name":"COGs", "value":valuestr}])
        await ctx.send(embed=embed)
    elif spec == "cmds":
        commands_list = [
            f"`{cmd.name}`  |  `{cmd.extras.get('group', 'No Group')}`  |  `{cmd.description if cmd.description else 'No Description'}`"
            for cmd in maybot.commands
        ]
        await paginate_commands(ctx, commands_list)
    elif any(spec.lower() == cog_name.lower() for cog_name in maybot.cogs.keys()):

        cog = maybot.get_cog(spec)

        if cog is None:
            for cog_instance in maybot.cogs.values():
                if hasattr(cog_instance, 'folder') and cog_instance.folder.lower() == spec.lower():
                    cog = cog_instance
                    break

        if cog:
            for cmd in maybot.commands:
                cmd_group = cmd.extras.get('group', 'No Group') if cmd.extras else 'No Group'
                if cmd_group.lower() == spec.lower():
                    cmd_desc = cmd.description if cmd.description else "No Description"
                    values.append(f"`{cmd.name}`: {cmd_desc}")
            valuestr = "- " + "\n- ".join(values)
            embed = create_embed(title=f"HELP PAGE | {cog.qualified_name} Commands", description=valuestr if len(valuestr) > 5 else "No commands in COG Group", color=disnake.Color.green())
            await ctx.send(embed=embed)
        else:
            await ctx.send("Cog not found. Make sure your casing is correct.")

    elif any(spec.lower() == cmd.name.lower() for cmd in maybot.commands):
        cmd = maybot.get_command(spec.lower())
        if cmd:
            cmd_desc = cmd.description if cmd.description else "No Description"
            cmd_group = cmd.extras.get('group', 'No Group') if cmd.extras else 'No Group'
            args = []
            for name, param in cmd.clean_params.items():
                if param.default is param.empty:
                    args.append(f"<{name}>")
                else:
                    args.append(f"[{name}]") 
            args_str = ' '.join(args)
            interpol = '\n- '.join(cmd.aliases)
            embed = create_embed(
                title=f"HELP PAGE | `{cmd.name}` Command",
                description=f"**Description:** {cmd_desc}\n**Group:** {cmd_group}\n**Usage:** `{cmd.name} {args_str}`\n**Aliases**:\n- {interpol}",
                color=disnake.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Command not found.")
    else:
        await ctx.send("ERR404: Request not found")


def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(help)
    return help
