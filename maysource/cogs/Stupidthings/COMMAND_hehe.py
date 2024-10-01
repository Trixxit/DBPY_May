from disnake.ext import commands
import disnake
from Utilities.staffchecks import Anystaffcheck, admin, mod, lcm
import asyncio

@commands.command()
@Anystaffcheck((admin, mod, lcm, 1231831222930636800))
async def hehe(ctx, user_id: int, *, message: str):
    user = await ctx.bot.fetch_user(user_id)
    if user:
        try:
            await user.send(message)
            await ctx.send(f":3 Sent message to {user.name} with id: {user_id}: \n{message}")
            await asyncio.sleep(3)
        except disnake.HTTPException as e:
            await ctx.send(f"Failed to send message to {user.name}: {e}")
    else:
        await ctx.send("User not found.")


def setup_command(cog):
    cog.bot.add_command(hehe)
    hehe.extras["example"] = "No Example Set"
    return hehe