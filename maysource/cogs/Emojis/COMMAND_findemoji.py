from disnake.ext import commands
import typing
import re
import difflib
import disnake
import asyncio

from Utilities.staffchecks import staffguideCheck

async def is_channel(ctx):
    return ctx.channel.id==1193586146450608148, 972408205990821908, 1186393899128852580
@commands.command(name='findemoji', description="Find an emoji from every server may is from")
@commands.check(is_channel)
@staffguideCheck()

async def findemoji(ctx, *, emoji_name: str):
    if not ctx.channel.id in [1193586146450608148, 972408205990821908, 1186393899128852580, 1191889768334774303] and ctx.author.id != 996395908654694430:
        await ctx.send("Not allowed in this channel, go to <#1193586146450608148>, <#972408205990821908>, <#1186393899128852580> or <#1191889768334774303>")
        return
    exact_match = None
    close_matches = []
    if emoji_name == "all":
        e = []
        for guild in ctx.bot.guilds:
            for emoji in guild.emojis:
                e.append(f"<:{emoji.name}:{emoji.id}>")
        count = 0
        p = "-# "
        for im in e:
            if count < 30:
                p += im
                count += 1
            elif count == 30:
                await ctx.send(p)
                p = "-# "
                count = 0
        return
    for guild in ctx.bot.guilds:
        for emoji in guild.emojis:
            if emoji.name.lower() == emoji_name.lower():
                exact_match = emoji
                break
            elif difflib.SequenceMatcher(None, emoji.name.lower(), emoji_name.lower()).ratio() >= 0.8 or emoji_name.lower() in emoji.name.lower():
                close_matches.append(emoji)
        if exact_match:
            break
    if exact_match:
        await ctx.send(f"\<:{emoji.name}:{emoji.id}>")
        await send_emoji_embed(ctx, exact_match)
    elif close_matches:
        close_matches_str = '\n'.join([f"{emoji.name} (ID: {emoji.id}) - {emoji.guild.name}" for emoji in close_matches])
        await ctx.send(f"Close matches found:\n{close_matches_str}")
    else:
        await ctx.send("No emoji found.")

async def send_emoji_embed(ctx, emoji):
    embed = disnake.Embed(title="Emoji Found", color=0x00ff00)
    embed.add_field(name="Name", value=emoji.name)
    embed.add_field(name="ID", value=str(emoji.id))
    embed.add_field(name="Usage", value=f"``<:{emoji.name}:{emoji.id}>``")
    embed.add_field(name="Emoji", value=f"<:{emoji.name}:{emoji.id}>")
    embed.add_field(name="Attachment Link", value=emoji.url)
    embed.add_field(name="Server", value=emoji.guild.name)
    embed.set_thumbnail(url=emoji.url)
    await ctx.send(embed=embed)

def setup_command(cog):
    cog.bot.add_command(findemoji)
    return findemoji