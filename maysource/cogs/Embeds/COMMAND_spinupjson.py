import disnake
from disnake.ext import commands
import asyncio
from Utilities.staffchecks import staffguideCheck
from Utilities.discord_utils import checkimgurl
import json
import tempfile
import aiofiles
import aiofiles.os as aios
import re

@commands.command(name="cj", description ="Use this command to be walked through a embed compiling chat, and then get it's JSON for an LG")
@staffguideCheck()
async def createjsonembed(ctx, number_of_embeds: int):
    if number_of_embeds < 1 or number_of_embeds > 10:
        await ctx.send("The number of embeds must be between 1 and 10.")
        return

    await ctx.send("Welcome to the embed compiler! Type `skip` when prompted to skip a step. `cancel` whenever to cancel the compiling. `json` to get the current JSON structure of the embed. `help` for detailed help!\n**Note: Input will move onto the next field after 10 minutes**")
    embed_creator = InteractiveEmbedCreation(ctx, ctx.bot, number_of_embeds)
    await embed_creator.create_embeds()


class InteractiveEmbedCreation:
    def __init__(self, ctx, bot, number_of_embeds):
        self.ctx = ctx
        self.bot = bot
        self.number_of_embeds = number_of_embeds
        self.embeds = [disnake.Embed() for _ in range(number_of_embeds)]
        self.current_step = 0


    async def send_initial_embed_message(self):
        try:
            embed = self.create_current_embed_preview()
            self.embed_message = await self.ctx.send(embed=embed)
        except Exception as e:
            embed = disnake.Embed(title="Current Embed Preview", color=disnake.Color.blue())
            self.embed_message = await self.ctx.send(embed=embed)
            print(e)

    def create_current_embed_preview(self):
        current_embed = self.embeds[self.current_step]
        return current_embed

    async def update_embed_message(self):
        try:
            embed = self.create_current_embed_preview()
            await self.embed_message.edit(embed=embed)
        except Exception as e:
            embed = disnake.Embed(title="Current Embed Preview", color=disnake.Color.blue())
            self.embed_message = await self.embed_message.edit(embed=embed)
            print(e)

    async def ask_for_input(self, prompt, check_length=None, check_format=None):
        rm = None
        rm = await self.ctx.send(prompt)

        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel

        emoji_id_pattern = re.compile(r"<:\w+:(\d+)>")
        emoji_name_pattern = re.compile(r":(\w+):")

        while True:
            try:
                message = await self.bot.wait_for('message', check=check, timeout=600.0)
                content = message.content
                if False:
                    for emoji_id_match in emoji_id_pattern.finditer(content):
                        emoji_id = emoji_id_match.group(1)
                        emoji = disnake.utils.get(self.bot.emojis, id=int(emoji_id))
                        if emoji and not message.author.premium_since:
                            content = content.replace(emoji_id_match.group(0), str(emoji))

                    for emoji_name_match in emoji_name_pattern.finditer(content):
                        emoji_name = emoji_name_match.group(1)
                        emoji = disnake.utils.get(self.bot.emojis, name=emoji_name)
                        if emoji and not message.author.premium_since:
                            content = content.replace(emoji_name_match.group(0), str(emoji))

                if content.lower() == 'cancel':
                    await self.ctx.send("Embed creation cancelled.")
                    return None
                if content.lower() == 'json':
                    embed_json = self.embeds[self.current_step].to_dict()
                    jstr = json.dumps(embed_json, indent=1)
                    temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False)
                    temp_file_path = temp_file.name
                    temp_file.close()
                    async with aiofiles.open(temp_file_path, 'w') as file:
                        await file.write(jstr)
                    await self.ctx.send("Here's the JSON object for the current embed object", file=disnake.File(temp_file_path, filename="output.txt"))
                    await aios.remove(temp_file_path)
                    await rm.delete()
                    rm = await self.ctx.send(prompt)
                    continue
                if content.lower() == 'help':
                    await self.ctx.send("# Help\nTitle: The title of the embed. Maximum character amount of `256` characters.\nDescription: The Body of the embed. Maximum character amount of `4090` characters.\nFields: Must contain a name and value, with optional inlining with eachother. Maximum name value is `256`, maximum value value is `1024`, inline is `yes` or `no`.\nColor: This should be the name of the color you want OR an rgb value seperated by spaces. E.g. `255 0 0`` or ``123 321 0`\nThumbnail / Image: These must be media attachment links, otherwise they'll be rejected. Please force-disembed with by surrounding the link with `<>`. E.g. `<https://cdn.discord.com/82237232123.png>`.\nAuthor: This appears above the title in small writing. Maximum value is `256` characters.\nFooter:Small text at the end of the embed. Max value of `256` characters.\nTimestamp: Adds the UTC.NOW timestamp to the embed.")
                if (check_length and len(content) > check_length) or (check_format and not check_format(content)):
                    await self.ctx.send("Invalid input. Please try again or type `cancel` to exit.")
                try:
                    await rm.delete()
                    await message.delete()
                except Exception as e:
                    print(e)
                return content
            except asyncio.TimeoutError:
                await self.ctx.send("Embed creation timed out.")
                return None

    async def add_color(self, embed):
        while True:
            color_input = await self.ask_for_input("Please enter a color name (e.g., `blue`, `red`) or RGB values separated by spaces (e.g., `255 0 0` for red). Type `skip` to skip or `cancel` to exit.")
            if color_input.lower() == 'skip':
                return
            elif color_input.lower() == 'cancel':
                raise Exception("Embed creation cancelled by user.")
            
            if ' ' in color_input:  # Check for RGB value input
                try:
                    r, g, b = map(int, color_input.split())
                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        color = disnake.Color.from_rgb(r, g, b)
                        embed.color = color
                        await self.update_embed_message()
                        break
                    else:
                        await self.ctx.send("RGB values must be in the range 0-255. Please try again.")
                except ValueError:
                    await self.ctx.send("Invalid RGB format. Please enter three numbers separated by spaces.")
            else:  # Check for color name input
                try:
                    color = getattr(disnake.Color, color_input.lower())()
                    embed.color = color
                    await self.update_embed_message()
                    break
                except AttributeError:
                    await self.ctx.send("Invalid color name. Please try again.")



    async def add_fields(self, embed):
        while True:
            num_fields = await self.ask_for_input("How many fields would you like to add? Enter a number, `skip` to skip, or `cancel` to exit.")
            if num_fields.lower() == 'skip':
                return
            elif num_fields.lower() == 'cancel':
                raise Exception("Embed creation cancelled by user.")
            try:
                num_fields = int(num_fields)
                for i in range(num_fields):
                    embed.add_field(name="THIS IS A PLACEHOLDER :D", value="THIS IS A PLACEHOLDER :D", inline=True)
                    await self.update_embed_message()
                for i in range(num_fields):
                    field_name = await self.ask_for_input(f"Enter name for field {i+1}:", 256)
                    embed.set_field_at(index=i, name=field_name, value="THIS IS A PLACEHOLDER :D")
                    await self.update_embed_message()
                    field_value = await self.ask_for_input(f"Enter value for field {i+1}:", 1024)
                    embed.set_field_at(index=i, name=field_name, value=field_value)
                    await self.update_embed_message()
                    field_inline = await self.ask_for_input(f"Should field {i+1} be inline? (`yes`/`no`):")
                    embed.set_field_at(index=i, name=field_name, value=field_value, inline=field_inline.lower()=="yes")
                    await self.update_embed_message()
                break
            except ValueError:
                await self.ctx.send("Invalid input. Please enter a valid number.")

    async def add_thumbnail(self, embed):
        while True:
            thumbnail_url = await self.ask_for_input("Enter the URL for the thumbnail (wrap the URL in `<` `>`). Type `skip` to skip this step.")
            if thumbnail_url.lower() == 'skip':
                return
            thumbnail_url = thumbnail_url.strip('<>')
            if (await checkimgurl(thumbnail_url)):
                embed.set_thumbnail(url=thumbnail_url)
                await self.update_embed_message()
                break
            else:
                await self.ctx.send("Invalid thumbnail attachment URL! Please try again:")

    async def add_image(self, embed):
        while True:
            image_url = await self.ask_for_input("Enter the URL for the image (wrap the URL in `<` `>`). Type `skip` to skip this step.")
            if image_url.lower() == 'skip':
                return
            image_url = image_url.strip('<>')
            if (await checkimgurl(image_url)):
                embed.set_image(url=image_url)
                await self.update_embed_message()
                break
            else:
                await self.ctx.send("Invalid image attachment URL! Please try again:")

    async def add_author(self, embed):
        author_name = await self.ask_for_input("Enter the author name. Type `skip` to skip this step.")
        if author_name.lower() == 'skip':
            return
        embed.set_author(name=author_name)
        await self.update_embed_message()

    async def add_footer(self, embed):
        footer_text = await self.ask_for_input("Enter the footer text. Type `skip` to skip this step.")
        if footer_text.lower() == 'skip':
            return
        embed.set_footer(text=footer_text)
        await self.update_embed_message()

    async def add_timestamp(self, embed):
        timestamp = await self.ask_for_input("Do you want to add the current timestamp to the embed? (`yes`/`no`)")
        if timestamp.lower() == 'yes':
            embed.timestamp = disnake.utils.utcnow()
            await self.update_embed_message()


    async def create_embeds(self):
        try:
            for index, embed in enumerate(self.embeds):
                await self.send_initial_embed_message()
                self.current_step = index
                title = await self.ask_for_input(f"Please insert the title for embed `{index + 1}`", check_length=256)
                if title is None:
                    return
                embed.title = title
                await self.update_embed_message()

                description = await self.ask_for_input(f"Please insert the description for embed `{index + 1}`", check_length=4090)
                if description is None:
                    return
                embed.description = description
                await self.update_embed_message()

                await self.add_color(embed)
                await self.add_fields(embed)
                await self.add_thumbnail(embed)
                await self.add_image(embed)
                await self.add_author(embed)
                await self.add_footer(embed)
                await self.add_timestamp(embed)

                embed_json = self.embeds[self.current_step].to_dict()
                jstr = json.dumps(embed_json, indent=1)
                temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False)
                temp_file_path = temp_file.name
                temp_file.close()
                async with aiofiles.open(temp_file_path, 'w') as file:
                    await file.write(jstr)
                await self.ctx.send("Heres the JSON object!", file=disnake.File(temp_file_path, filename="output.json"))
                await aios.remove(temp_file_path)
                return
        except Exception as e:
            print(f"Error occured in stepstep embed creation: {e}")
            await self.ctx.send(f"I ran into an error...")


def setup_command(cog):
    cog.bot.add_command(createjsonembed)
    return createjsonembed