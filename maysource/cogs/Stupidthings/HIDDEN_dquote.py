from disnake.ext import commands
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from Utilities.staffchecks import admin, lcm, cm, mod, Anystaffcheck
from Utilities.json_methods import read_json, maptoJSON
import disnake
import os
import aiofiles


access_key = "BSQypzYqutsIZjYicgRWsBsOdNdcTWkEz2rzP1uIr2g"
url = 'https://api.unsplash.com/photos/random'
params = {
    'query': 'landscape',
    'orientation': 'landscape',
    'client_id': access_key
}

def wrap_text(text, max_chars):
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        if sum(len(w) for w in current_line) + len(word) + len(current_line) - 1 < max_chars:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines


@commands.command(name='dquote', description="Summons a random user quote")
@commands.cooldown(1, 10, commands.BucketType.default)
@Anystaffcheck((admin, mod, lcm, cm, 1180945644567941272, 1196465778438963392))
async def dquote(ctx, specifier: int = -1):
    await ctx.send("Generating...")
    data = await read_json(maptoJSON("stuff.json"))
    quote = random.choice(data["Quotes"])
    if specifier > 0 and specifier < len(data["Quotes"]):
        quote = data["Quotes"][specifier]
    response = requests.get(url, params=params)
    if response.status_code != 200:
        await ctx.send("Failed to download image from Unsplash.")
        return

    data = response.json()
    image_url = data.get('urls', {}).get('regular')
    if not image_url:
        await ctx.send("Downloaded image URL was null.")
        return
    
    image_response = requests.get(image_url)
    if image_response.status_code != 200:
        await ctx.send("Failed to download the actual image.")
        return
    
    image = Image.open(BytesIO(image_response.content))
    draw = ImageDraw.Draw(image)
    width, height = image.size
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "arial.ttf")
    font_path_bi = os.path.join(current_dir, "arialbi.ttf")
    font_size = 40
    font = ImageFont.truetype(font_path_bi, font_size)
    small_font = ImageFont.truetype(font_path, 20)
    acredit = f"{data['user']['name']} @ Unsplash"

    max_chars = width // (font_size // 2) 
    wrapped_text = wrap_text(quote, max_chars)

    text_x, text_y = 20, height / 2 - 30
    for line in wrapped_text:
        draw.text((text_x, text_y), line, font=font, fill=(255,255,255))
        text_y += font_size 

    credits_x, credits_y = 20, height - 40  

    draw.text((credits_x, credits_y), acredit, font=small_font, fill=(255,255,255))
    await send_image_and_delete(ctx, image)


async def send_image_and_delete(ctx, image):
    temp_image_path = 'temp_quote_image.png'
    image.save(temp_image_path, 'PNG')
    await ctx.send(file=disnake.File(temp_image_path, filename='quote_image.png'))
    await aiofiles.os.remove(temp_image_path)


def setup_command(cog):
    cog.bot.add_command(dquote)
    dquote.extras["example"] = "No Example Set"
    return dquote