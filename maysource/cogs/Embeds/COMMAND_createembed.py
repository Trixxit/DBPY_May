from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck, admin, leadguide, guide
import disnake
from disnake.ext import commands
import json

@commands.command(name='jembed')
@Anystaffcheck((admin, leadguide, guide))
async def jsonembed(ctx, channel_id: int, *, json_str: str = None):
    try:
        channel = ctx.bot.get_channel(channel_id)
        if channel is None or not isinstance(channel, disnake.abc.Messageable):
            await ctx.send("Channel or thread not found.")
            return

        if json_str is None:
            if ctx.message.attachments:
                attachment = ctx.message.attachments[0]
                if attachment.filename.endswith(('.json', '.txt')):
                    json_str = (await attachment.read()).decode('utf-8')
                else:
                    await ctx.send("Please provide a JSON or TXT file as an attachment.")
                    return
            else:
                await ctx.send("Please provide the embed data as JSON string or attachment.")
                return

        embed_data = json.loads(json_str)
        if isinstance(embed_data, list): 
            embeds = [disnake.Embed.from_dict(data) for data in embed_data]
        else: 
            embeds = [disnake.Embed.from_dict(embed_data)]
        for embed in embeds:
            await channel.send(embed=embed)

        await ctx.send(f"Embed(s) sent to {channel.mention}.")
    except json.JSONDecodeError:
        await ctx.send("Invalid JSON format.")
    except disnake.Forbidden:
        await ctx.send("I don't have permission to send messages in that channel or thread.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

def setup_command(cog):
    cog.bot.add_command(jsonembed)
    return jsonembed
