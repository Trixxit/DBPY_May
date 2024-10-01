from disnake.ext import commands
import disnake
from Utilities.staffchecks import Anystaffcheck
from Utilities.json_methods import read_json, write_json, maptoJSON
import re
from datetime import datetime, timedelta
from disnake import Embed

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


@commands.command(name='editrole', description="gwah")
#@Anystaffcheck((1231831222930636800, 971704489520300032))
async def editrole(ctx):
    cool = await read_json(maptoJSON("cool.json"))
    if str(ctx.author.id) in cool.keys():
        current_time = datetime.now()
        if datetime.strptime(cool[str(ctx.author.id)], '%Y-%m-%dT%H:%M:%S.%f') > current_time:
            done = datetime.fromisoformat(cool[str(ctx.author.id)])
            await ctx.send(f"<@{ctx.author.id}> you are still on cooldown! You will be able to execute this command <t:{int(done.timestamp())}:R>")
            return
    data = (await read_json(maptoJSON("rolestuff.json")))
    if str(ctx.author.id) in data["blacklisted"]:
        await ctx.send("You're.. blacklisted... why did you think this would work???")
        return
    if str(ctx.author.id) in data["customrolestuff"]:
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        role_data = data["customrolestuff"][str(ctx.author.id)]
        role_name = role_data["name"]
        role_color = role_data["color"]
        role_icon = role_data["icon"]
        expiry_date = datetime.fromisoformat(role_data["expiry"])
        expiry_relative = f"<t:{int(expiry_date.timestamp())}:R>"
        expiry_long = f"<t:{int(expiry_date.timestamp())}:F>"
        
        embed = Embed(title=role_name, color=int(role_color) if role_color != "default" else None)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        """
        if role_icon.startswith("<:"):
            icon_id = role_icon.split(':')[-1][:-1]
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{icon_id}.png")
        elif role_icon.startswith("<a:"):
            icon_id = role_icon.split(':')[-1][:-1]
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{icon_id}.gif")
        """
        role = ctx.guild.get_role(role_data["id"])
        if role.icon != None:
            iconurl = role.icon.url
            embed.set_thumbnail(url=f"{iconurl}")
        if role_color != "default":
            role_color=int(role_color)
            embed.add_field(name="Colour", value="#" + role_data["color"])
        embed.add_field(name="Expiry Date", value=f"{expiry_long} ({expiry_relative})")
        
        await ctx.send(embed=embed)
        

        roleid = role_data["id"]
        role = ctx.guild.get_role(roleid)
        sett = False
        await ctx.send("Please enter the name for the custom role:")
        role_name_msg = await ctx.bot.wait_for('message', check=check)
        role_nam = role_name_msg.content
        if role_nam != role_name and role_nam != "skip":
            sett = True
            



        await ctx.send("Please enter the non-animated custom emoji/attachment for the role icon: (attachment is better \:) )")
        role_icon_msg = await ctx.bot.wait_for('message', check=check)
        role_icon_c = role_icon_msg.content if role_icon_msg.content != '.' else None
        role_ico = None
        if len(role_icon_msg.attachments) > 0:
            role_ico= await role_icon_msg.attachments[0].read(use_cached=True)
        elif role_icon_c:
            role_ico = disnake.PartialEmoji.from_str(role_icon_c)
            role_ico._state = ctx.bot._connection
            print(role_ico.name)
        

        if role_color != "default":
            await ctx.send("Please enter the color for the role (in hex, e.g., #ff5733): ('skip' to retain original)")
            role_color_msg = await ctx.bot.wait_for('message', check=check)
            if not "skip" in role_color_msg.content:
                try:
                    role_color_msg.content = role_color_msg.content.replace("#", "")
                    role_color = int(role_color_msg.content.lstrip('#'), 16)
                except:
                    role_color = disnake.Colour.default()
                    await ctx.send("Invalid color, doing default.")
            else:
                role_color = int(str(role_color).lstrip('#'), 16)
        

        await ctx.send("Are you sure you want to save changes? ('yes' to confirm, 'no' to exit)")
        con = await ctx.bot.wait_for('message', check=check)
        if not 'yes' in con.content.lower():
            return
        if sett == True:
            await role.edit(name=role_nam if role_nam != "skip" else role_name)
        await role.edit(icon=role_ico)
        await role.edit(color=int(role_color) if role_color != "default" else disnake.Colour.default())
        thetimein12hours = datetime.now() + timedelta(hours=12)
        thetimein12hours_str = thetimein12hours.isoformat()
        cool[str(ctx.author.id)] = thetimein12hours_str
        await write_json(maptoJSON("cool.json"), cool)
        await ctx.send(f"<@{ctx.author.id}> cooldown set! You will be able to execute this command 12 hours")
        role_data = data["customrolestuff"][str(ctx.author.id)]
        expiry_date = datetime.fromisoformat(role_data["expiry"])
        expiry_long = f"<t:{int(expiry_date.timestamp())}:F>"
        await ctx.send(f"Custom role '{role_name}' edited successfully! You may enjoy it for {expiry_long} c:")
        await (ctx.guild.get_channel(1211187631346552872)).send(f"<@996395908654694430>, <@{ctx.author.id}> has edited role {role_name} with colour #{role_color}")
        await (ctx.guild.get_channel(1256290638937198673)).send(f"<@676939535241707521>, <@{ctx.author.id}> has edited role {role_name} with colour #{role_color}")
        
        data["customrolestuff"][str(ctx.author.id)] = {
            "name": role_nam,
            "id": role.id,
            "color": str(role_color) if role_color != "default" else "default",
            "icon": role_icon_msg.content,
            "expiry": role_data["expiry"]
        }
        await write_json(maptoJSON("rolestuff.json"), data)

        data = (await read_json(maptoJSON("rolestuff.json")))
        role_data = data["customrolestuff"][str(ctx.author.id)]
        role_name = role_data["name"]
        role_color = role_data["color"]
        role_icon = role_data["icon"]
        expiry_date = datetime.fromisoformat(role_data["expiry"])
        expiry_relative = f"<t:{int(expiry_date.timestamp())}:R>"
        expiry_long = f"<t:{int(expiry_date.timestamp())}:F>"
        
        embed = Embed(title=role_name, color=int(role_color) if role_color != "default" else None)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        """
        if role_icon.startswith("<:"):
            icon_id = role_icon.split(':')[-1][:-1]
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{icon_id}.png")
        elif role_icon.startswith("<a:"):
            icon_id = role_icon.split(':')[-1][:-1]
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{icon_id}.gif")
        """
        if role.icon != None:
            iconurl = role.icon.url
            embed.set_thumbnail(url=f"{iconurl}")
        embed.set_thumbnail(url=f"{iconurl}")
        if role_color != "default":
            role_color=int(role_color)
            embed.add_field(name="Colour", value="#" + role_data["color"])
        embed.add_field(name="Expiry Date", value=f"{expiry_long} ({expiry_relative})")
        
        
        await ctx.send(embed=embed)



        
    else:
        await ctx.send("You do not have the necessary role to use this command.")


def setup_command(cog):
    cog.bot.add_command(editrole)
    editrole.extras["example"] = "No Example Set"
    return editrole