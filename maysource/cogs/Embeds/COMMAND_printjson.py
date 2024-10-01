import disnake
from disnake.ext import commands
from Utilities.staffchecks import staffguideCheck
import json
import tempfile
import aiofiles
import aiofiles.os as aios

@commands.command(name='printjson')
@staffguideCheck()
async def printjson(ctx, channel_id: int, message_id: int):
    try:
        channel = ctx.bot.get_channel(channel_id)
        if channel is None or not isinstance(channel, disnake.abc.Messageable):
            await ctx.send("Channel or thread not found.")
            return

        message = await channel.fetch_message(message_id)
        if not message.embeds:
            await ctx.send("No embeds found in the specified message.")
            return

        embed_json = [embed.to_dict() for embed in message.embeds]
        embed_json_str = json.dumps(embed_json, indent=4)

        if len(embed_json_str) > 1900:
            temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False)
            temp_file_path = temp_file.name
            temp_file.close()
            async with aiofiles.open(temp_file_path, 'w') as file:
                await file.write(embed_json_str)
            await ctx.send(file=disnake.File(temp_file_path, filename="output.json"))
            await aios.remove(temp_file_path)
            temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False)
            temp_file_path = temp_file.name
            temp_file.close()
            async with aiofiles.open(temp_file_path, 'w') as file:
                await file.write(embed_json_str)
            await ctx.send(file=disnake.File(temp_file_path, filename="output.txt"))
            await aios.remove(temp_file_path)
        else:
            await ctx.send(f"```json\n{embed_json_str}\n```")

    except disnake.Forbidden:
        await ctx.send("I don't have permission to access that channel or message.")
    except disnake.NotFound:
        await ctx.send("Message not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

def setup_command(cog):
    cog.bot.add_command(printjson)
    return printjson