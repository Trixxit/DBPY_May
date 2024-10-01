import disnake
from disnake.ext import commands
import asyncio
from Utilities.staffchecks import Anystaffcheck
import json
import tempfile
import aiofiles
import aiofiles.os as aios

@commands.command(name="editembed")
@Anystaffcheck((1231831222930636800, 1180945644567941272))
async def editembed(ctx, channel_id: int, message_id: int):
    try:
        channel = await ctx.guild.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)
    except disnake.NotFound:
        await ctx.send("Message not found.")
        return
    except disnake.HTTPException:
        await ctx.send("Failed to fetch message.")
        return

    if not message.embeds:
        await ctx.send("No embeds found in the message.")
        return

    embed_editor = InteractiveEmbedEditing(ctx, ctx.bot, message)
    await embed_editor.edit_embeds()

class InteractiveEmbedEditing:
    def __init__(self, ctx, bot, message):
        self.ctx = ctx
        self.bot = bot
        self.message = message
        self.embeds = message.embeds


    async def edit_fields(self, embed):
        while True:
            field_choice = await self.ask_for_input(
                "Enter `add` to add a new field, `edit <number>` to edit a field, `remove <number>` to remove a field, or `done` to finish.")
            if field_choice is None or field_choice.lower() == 'done':
                break
            elif field_choice.lower().startswith('add'):
                await self.add_field(embed)
            elif field_choice.lower().startswith('edit'):
                await self.edit_field(embed, field_choice)
            elif field_choice.lower().startswith('remove'):
                await self.remove_field(embed, field_choice)

    async def add_field(self, embed):
        field_name = await self.ask_for_input("Enter field name:")
        field_value = await self.ask_for_input("Enter field value:")
        field_inline = await self.ask_for_input("Is the field inline? (yes/no):")
        if field_name and field_value:
            embed.add_field(name=field_name, value=field_value, inline=field_inline.lower() == 'yes')

    
    def parse_color(self, color_str):
        if color_str.startswith("#") and len(color_str) == 7:
            # Hex color
            return disnake.Color(int(color_str[1:], 16))
        elif color_str.startswith("rgb"):
            # RGB color
            rgb_values = color_str.strip("rgb()").split(",")
            if len(rgb_values) == 3 and all(v.isdigit() for v in rgb_values):
                return disnake.Color.from_rgb(*map(int, rgb_values))
        else:
            color = getattr(disnake.Color, color_str.lower(), None)
            if color:
                return color()
        return None

    async def edit_embeds(self):
        embed_index = 0
        if len(self.embeds) > 1:
            embed_index = await self.select_embed(self)
            if embed_index is None:
                return

        current_embed = self.embeds[embed_index]
        while True:
            choice = await self.ask_for_input(
                "What would you like to edit? (`title`, `description`, `color`, `fields`, `author`, `footer`.) Type `finish` to save changes or `cancel` to discard.")
            if choice is None or choice.lower() == 'cancel':
                await self.ctx.send("Changes discarded.")
                return
            elif choice.lower() == 'finish':
                await self.save_changes(embed_index)
                break
            elif choice.lower() == 'title':
                new_title = await self.ask_for_input("Enter the new title:")
                if new_title is not None:
                    current_embed.title = new_title

            elif choice.lower() == 'description':
                new_description = await self.ask_for_input("Enter the new description:")
                if new_description is not None:
                    current_embed.description = new_description

            elif choice.lower() == 'color':
                new_color = await self.ask_for_input("Enter the new color (hex, RGB, or Disnake color name):")
                if new_color is not None:
                    current_embed.color = self.parse_color(new_color)    
            elif choice.lower() == 'image':
                new_image_url = self.ctx.message.attachments[0]
                current_embed.set_image(new_image_url)
            else:
                await self.ctx.send("Invalid choice.")

    async def ask_for_input(self, prompt, check_length=None, check_format=None):
        await self.ctx.send(prompt)

        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel

        while True:
            try:
                message = await self.bot.wait_for('message', check=check, timeout=600.0)
                content = message.content
                if content.lower() == 'cancel':
                    return None
                if (check_length and len(content) > check_length) or (check_format and not check_format(content)):
                    await self.ctx.send("Invalid input. Please try again.")
                    continue
                return content
            except asyncio.TimeoutError:
                await self.ctx.send("Prompt timed out.")
                return None

    async def select_embed(self):
        def lecheck(strig: str):
            try:
                int(strig)
            except:
                return False
            else:
                if int(strig) > 0 and int(strig) < len(self.embeds):
                    return True
            return False

        while True:
            choice = await self.ask_for_input(f"Which embed would you like to edit? (1 - {len(self.embeds)})", 10, lecheck)
        return int(choice) - 1 if choice else None



def setup_command(cog):
    cog.bot.add_command(editembed)
    return editembed