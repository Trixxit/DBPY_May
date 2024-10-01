from disnake.ext import commands
from Utilities.staffchecks import admincheck
import aiohttp

maybot = None

@commands.command(name='changepfp', description="Changes May's pfp")
@admincheck()
async def changepfp(ctx, url: str = None):
        global maybot
        if ctx.message.attachments:
            image_data = await ctx.message.attachments[0].read()
        elif url:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                    else:
                        await ctx.send("Failed to fetch image from the provided URL.")
                        return
        else:
            await ctx.send("Please provide an image URL or attach an image.")
            return

        try:
            await maybot.user.edit(avatar=image_data)
            await ctx.send("Avatar changed successfully.")
        except Exception as e:
            await ctx.send(f"Failed to change avatar: {e}")

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(changepfp)
    return changepfp