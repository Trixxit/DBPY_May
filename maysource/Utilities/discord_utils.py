import disnake
from disnake import Embed
import re
import aiohttp
import random
from typing import Optional, Union, List
import tempfile
import asyncio
import aiofiles
import aiofiles.os as aios


mes_con = [

]


def getMesCon() -> List:
    return mes_con

def mprint(message) -> None:
    print(message)
    mes_con.append(str(message))
    if (len(mes_con) > 50):
        mes_con.pop(0)
   

def sanmes(message):
    sanitized_message = message.replace("@", "@\u200b").replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere").replace("**", "")
    role_mentions = re.findall(r'<@&(\d+)>', sanitized_message)
    sanitized_message = sanitized_message.replace(f"/", f"\/")
    sanitized_message = sanitized_message.replace(f".", f"\.")
    sanitized_message = sanitized_message.replace(f"@", f"\@")
    sanitized_message = sanitized_message.replace(f"|", f"\|")
    sanitized_message = sanitized_message.replace(f"^", f"\^")
    sanitized_message = sanitized_message.replace(f"!", f"\!")
    sanitized_message = sanitized_message.replace(f"$", f"\$")
    sanitized_message = sanitized_message.replace(f":", f"\:")
    sanitized_message = sanitized_message.replace(f"[", f"\[")
    sanitized_message = sanitized_message.replace(f"]", f"\]")
    for role_id in role_mentions:
        role = ctx.guild.get_role(int(role_id))
        if role:
            sanitized_message = sanitized_message.replace(f"<@&{role_id}>", f"@\u200b{role.name}")
        else:
            sanitized_message = sanitized_message.replace(f"<@&{role_id}>", f"@\u200b{role_id}")
    return sanitized_message


def create_embed(title: str = "", 
                 description: str = "", 
                 color: Union[int, disnake.Color] = disnake.Color.blue(), 
                 fields: Optional[List[dict]] = None,
                 thumbnail_url: Optional[str] = None, 
                 image_url: Optional[str] = None,
                 author: Optional[dict] = None, 
                 footer: Optional[dict] = None,
                 timestamp: Optional[bool] = False) -> disnake.Embed:
    """
    Create a Discord embed with various options.

    :param title: Title of the embed.
    :param description: Description of the embed.
    :param color: Color of the embed. Defaults to blue.
    :param fields: List of fields to add to the embed. Each field should be a dictionary with 'name', 'value', and optionally 'inline'.
    :param thumbnail_url: URL of the thumbnail image.
    :param image_url: URL of the image to display in the embed.
    :param author: Dictionary with 'name', 'url', and 'icon_url' to set the author of the embed.
    :param footer: Dictionary with 'text' and 'icon_url' for the footer.
    :param timestamp: Whether to add the current timestamp to the embed.
    :return: A disnake.Embed object.
    """

    embed = Embed(title=title, description=description, color=color)

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    if image_url:
        embed.set_image(url=image_url)

    if author:
        embed.set_author(name=author.get("name"), url=author.get("url"), icon_url=author.get("icon_url"))

    if footer:
        embed.set_footer(text=footer.get("text"), icon_url=footer.get("icon_url"))

    if fields:
        for field in fields:
            embed.add_field(name=field.get("name"), value=field.get("value"), inline=field.get("inline", False))

    if timestamp:
        embed.timestamp = disnake.utils.utcnow()

    return embed

async def checkimgurl(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:[^:@]+:[^:@]+@)?'
        r'(?:[\w-]+(?:(?:\.[\w-]+)+))'  
        r'(?::\d+)?'  
        r'(?:/[\w-]+)*'  
        r'(?:\.(?:jpg|gif|png|jpeg))'  
        r'(?:\?.+)?$',  
        re.IGNORECASE)

    if re.match(regex, url) is None:
        return False

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200 and 'image' in response.headers.get('Content-Type', ''):
                    return True
    except Exception as e:
        print(f"Error checking image URL: {e}")

    return False

def randcolor() -> disnake.Colour:
    return disnake.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

async def sendfile(content: str, ctx, message: str = "", name: str = "temp", ext: str = ".txt") -> None:
    try:
        temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix=ext, delete=False)
        temp_file_path = temp_file.name 
        temp_file.close()
        async with aiofiles.open(temp_file_path, 'w') as file:
            await file.write(content)
        await ctx.send(message if message else "Here ya go!", file=disnake.File(temp_file_path, filename=name + ext))
        await aios.remove(temp_file_path)
    except disnake.HTTPException as e:
        print(f"HTTPException: Response: {e.response}, Message: {e.text}")
        try:
                await ctx.send("Something went wrong...")
                await aios.remove(temp_file_path)
        except:
                pass
    except Exception as e:
        print(f"An unexpected exception occurred: {e}")
        try:
                await ctx.send("Something went wrong...")
                await aios.remove(temp_file_path)
        except:
                pass