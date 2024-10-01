import re
import aiohttp
import disnake
from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import asyncio

EMOJI_ID_REGEX = r"<a?:[a-zA-Z0-9_]+:(\d+)>"

@commands.command(name="addemoji", description="Add emojis through links, existing externals or attachments!")
@Anystaffcheck((1231831222930636800, 1183808147568210050, 1180945644567941272))
#@staffguideCheck()
async def stealemoji(ctx, *args: str):
    if not ctx.message.attachments and not args:
        await ctx.send("Please provide either attachments, emoji URLs, or raw emojis.")
        return

    attachments = ctx.message.attachments
    all_emojis = attachments + list(args)
    successfully_added_emojis = []

    async with aiohttp.ClientSession() as session:
        for emoji in all_emojis:
            try:
                if isinstance(emoji, disnake.Attachment):
                    emoji_bytes = await emoji.read()
                    emoji_name = emoji.filename.split('.')[0]
                else:
                    emoji_id_match = re.match(EMOJI_ID_REGEX, emoji)
                    if emoji_id_match:
                        emoji_id = emoji_id_match.group(1)
                        emoji_ext = "gif" if emoji.startswith("<a:") else "png"
                        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{emoji_ext}"
                    else:
                        emoji_url = emoji

                    async with session.get(emoji_url) as response:
                        if response.status != 200:
                            raise Exception("Failed to fetch emoji.")
                        emoji_bytes = await response.read()
                        emoji_name = emoji_url.split('/')[-1].split('.')[0]

                created_emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=emoji_bytes)
                await ctx.send(f"Added emoji: {created_emoji}")
                if created_emoji:
                    successfully_added_emojis.append(created_emoji)
            except disnake.HTTPException as e:
                if e.code == 30008: 
                    await ctx.send("Maximum number of emojis reached. Cannot add more.")
                    break
                else:
                    await ctx.send(f"Failed to add emoji: {e.text}")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")
    if len(successfully_added_emojis) > 0:
        await ctx.send("Do you want to rename all added emojis? Reply with 'yes' to proceed.")
        try:
            confirmation = await ctx.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60.0
            )
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Skipping renaming process.")
            return

        if confirmation.content.lower() == "yes":
            await ctx.send(f"Please send {len(successfully_added_emojis)} single-word names, separated by spaces.")

            try:
                names_msg = await ctx.bot.wait_for(
                    "message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60.0
                )
            except asyncio.TimeoutError:
                await ctx.send("Timed out. Skipping renaming process.")
                return

            new_names = names_msg.content.replace(",", "").split()

            if len(new_names) != len(successfully_added_emojis):
                await ctx.send("The number of names provided does not match the number of emojis. Skipping renaming process.")
                return

            for emoji, new_name in zip(successfully_added_emojis, new_names):
                try:
                    await emoji.edit(name=new_name)
                    await ctx.send(f"Emoji {emoji} renamed to {new_name}.")
                except disnake.HTTPException as e:
                    await ctx.send(f"Failed to rename emoji {emoji}: {e.text}")


def setup_command(cog):
    cog.bot.add_command(stealemoji)
    return stealemoji