from disnake.ext import commands
import disnake
from Utilities.staffchecks import Anystaffcheck
from Utilities.json_methods import read_json, write_json, maptoJSON
import re
from datetime import datetime, timedelta

def ffi(input_string):
    pattern1 = r"<:(\w+):(\d+)>"
    pattern2 = r":(\w+):"
    
    match = re.search(pattern1, input_string)
    if match:
        return match.group(1), match.group(2)
    
    match = re.search(pattern2, input_string)
    if match:
        return match.group(1), None
    
    return None, None


@commands.command(name='customrole', description="gwah")
#@Anystaffcheck((1231831222930636800, 971704489520300032))
async def customrole(ctx):
    role_queue_1 = disnake.utils.get(ctx.guild.roles, id=1251020199042486283)
    role_queue_2 = disnake.utils.get(ctx.guild.roles, id=1251020805433720853)
    r1 = True if role_queue_1 in ctx.author.roles else False
    r2 = True if role_queue_2 in ctx.author.roles else False
    data = (await read_json(maptoJSON("rolestuff.json")))
    if str(ctx.author.id) in data["blacklisted"]:
        await ctx.send("You're.. blacklisted... why did you think this would work???")
        return
    if r1 or r2:
        if str(ctx.author.id) in data["customrolestuff"]:
            await ctx.send("You already have a custom role, smh!")
            return
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("Please enter the name for the custom role:")
        role_name_msg = await ctx.bot.wait_for('message', check=check)
        role_name = role_name_msg.content


        await ctx.send("Please enter the emoji/attachment for the role icon:")
        role_icon_msg = await ctx.bot.wait_for('message', check=check)
        role_icon_c = role_icon_msg.content if role_icon_msg.content != '.' else None
        role_ico = None
        if len(role_icon_msg.attachments) != 0:
            role_ico=await role_icon_msg.attachments[0].read(use_cached=True)
        elif role_icon_c:
            role_ico = disnake.PartialEmoji.from_str(role_icon_c)
            role_ico._state = ctx.bot._connection
            print(role_ico.name)

        role_color = disnake.Colour.default()
        if r2:
            
            await ctx.send("Please enter the color for the role (in hex, e.g., #ff5733):")
            role_color_msg = await ctx.bot.wait_for('message', check=check)
            try:
                role_color_msg.content = role_color_msg.content.replace("#", "")
                role_color = int(role_color_msg.content.lstrip('#'), 16)
            except:
                role_color = disnake.Colour.default()
                await ctx.send("Invalid color, doing default.")

        reference_role = ctx.guild.get_role(1251382343621673051)
        position = reference_role.position - 1

        role = await ctx.guild.create_role(
            name=role_name, 
            color=disnake.Colour(role_color) if r2 else role_color,
            icon=role_ico,
        )
        await ctx.guild.edit_role_positions(positions={role: position})

        await ctx.author.add_roles(role)
        await ctx.send(f"Custom role '{role_name}' created successfully! You may enjoy it for 31 days c:")
        await (ctx.guild.get_channel(1211187631346552872)).send(f"<@996395908654694430>, <@{ctx.author.id}> has made role {role_name} with colour #{role_color}, at position {position}")
        await (ctx.guild.get_channel(1256290638937198673)).send(f"<@676939535241707521>, <@{ctx.author.id}> has made role {role_name} with colour #{role_color}, at position {position}")
        if r1:
            await ctx.author.remove_roles(role_queue_1)
        if r2:
            await ctx.author.remove_roles(role_queue_2)

        thetimein30days = datetime.now() + timedelta(days=30)
        thetimein30days_str = thetimein30days.isoformat()
        data["customrolestuff"][str(ctx.author.id)] = {
            "name": role_name,
            "id": role.id,
            "color": str(role_color) if r2 else "default",
            "icon": role_icon_msg.content,
            "expiry": thetimein30days_str
        }
        await write_json(maptoJSON("rolestuff.json"), data)
    else:
        await ctx.send("You do not have the necessary role to use this command.")


def setup_command(cog):
    cog.bot.add_command(customrole)
    customrole.extras["example"] = "No Example Set"
    return customrole