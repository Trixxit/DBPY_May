from disnake.ext import commands
import disnake
from Utilities.staffchecks import Anystaffcheck, admin, mod, lcm
import asyncio

@commands.command()
@Anystaffcheck((admin, mod, lcm))
async def embedmake(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    await ctx.send(f"{ctx.author.mention}, enter the channel id please :)")
    try:
        c = await ctx.bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, you did not say a id")
        return
    await ctx.send(f"{ctx.author.mention}, enter the title please :)")
    try:
        t = await ctx.bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, you did not say a title for the embed")
        return
    target = ctx.bot.get_channel(int(c.content))
    await ctx.send(f"{ctx.author.mention}, enter the description please :)")
    try:
        d = await ctx.bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, you did not say a description for the embed")
        return
    a = ctx.message.attachments
    
    embeder = []
    if a:
            for keyed in a:
                embed = disnake.Embed(title=t.content, description=d.content, url=ctx.channel.jump_url)
                embed.set_image(url=keyed.url)
                embeder.append(embed)
    else:
        embed = disnake.Embed(title=t.content, description=d.content, url=ctx.channel.jump_url)
        embeder.append(embed)
    await target.send(embeds=embeder)
    


def setup_command(cog):
    cog.bot.add_command(embedmake)
    embedmake.extras["example"] = "No Example Set"
    return embedmake