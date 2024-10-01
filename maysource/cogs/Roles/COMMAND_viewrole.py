from disnake.ext import commands
from Utilities.json_methods import read_json, maptoJSON
from disnake import Embed
import datetime
import disnake

@commands.command(name='viewrole', description="nyan")
@commands.cooldown(1, 10, commands.BucketType.user)
async def viewrole(ctx, member: disnake.Member = None):
    data = await read_json(maptoJSON("rolestuff.json"))
    if member == None:
        user_id = str(ctx.author.id)
    else:
        user_id = str(member.id)
    
    if user_id in data["customrolestuff"]:
        role_data = data["customrolestuff"][user_id]
        role_name = role_data["name"]
        role_color = int(role_data["color"]) if role_data["color"] != "default" and role_data["color"] != "000000" else None
        role_icon = role_data["icon"]
        expiry_date = datetime.datetime.fromisoformat(role_data["expiry"])
        expiry_relative = f"<t:{int(expiry_date.timestamp())}:R>"
        expiry_long = f"<t:{int(expiry_date.timestamp())}:F>"
        
        embed = Embed(title=role_name, color=role_color)
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
        embed.add_field(name="Colour", value="#" + role_data["color"])
        embed.add_field(name="Expiry Date", value=f"{expiry_long} ({expiry_relative})")
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have a custom role!")

def setup_command(cog):
    cog.bot.add_command(viewrole)
    viewrole.extras["example"] = "No Example Set"
    return viewrole
