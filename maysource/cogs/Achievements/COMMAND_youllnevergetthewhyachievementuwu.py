import random
from disnake.ext import commands
import asyncio
import disnake
import validators
import re

from Utilities.json_methods import maptoJSON, read_json
from Utilities.staffchecks import user_has_role

roles = (
    "blessed by rng",
    "why..?",
    "truly insane",
    "insanity",
    "cornucopia",
    "prequelmon master",
    "caught them all",
    "gear loyalist",
    "easter egg hunter",
    "heavenly protection",
    "extinction",
    "wan piece enthusiast",
    "stamp collector",
    "beginners luck",
    "cant touch this",
    "carnelian",
    "square",
    "apex warrior",
    "rechord",
    "prequel of legends",
    "pop culture",
    "chimera",
    "gladiator",
    "tria",
    "berserker",
    "john wick",
    "fanboy",
    "huh?!",
    "功夫",
    "epic!"
)

@commands.command(name='submit', description="Submit an attachment for evaluation! Please include your video / photo as an attachment(s) or as a single link, and the name of the role you want!")
async def youllnevergetthewhyachievementuwu(ctx, link: str = None):
    if user_has_role(ctx.author, (1194556618860400701, 1)):
        await ctx.send("You've been blacklisted!")
        return
    
    randint = random.randint(1000000000, 9999999999)

    if link and link.lower() == "list":
        rah = '\n- '.join(roles)
        await ctx.send(f"```- {rah}```")
        return

    dup = ctx.message

    data = await read_json(maptoJSON("achi.json"))
    if str(ctx.author.id) not in data["IDs"].keys():
        await ctx.send(f"{ctx.author.mention}, You haven't bound your PID yet! Use ``>>bind <PID>`` (e.g: ``>>bind 1234567``) to bind it!")
        return

    PlayerID = data["IDs"][str(ctx.author.id)]

    if len(dup.attachments) < 1 and not link:
        await ctx.send(f"{ctx.author.mention}, You must attach a file or a link!")
        return

    if dup.attachments:
        if any(attachment.size > 8000000 for attachment in dup.attachments):
            await ctx.send(f"{ctx.author.mention}, One or more attached files are too large to send. Please use files smaller than 8MB.")
            return
    elif link:
        if re.match(r'https?://(www\.)?discord\.com/channels/\d+/\d+/\d+', link):
            await ctx.send(f"{ctx.author.mention}, Message redirection links are not allowed, if you've submitted proof publicly for a HA please delete it or face consequences.")
            return
        elif not validators.url(link):
            await ctx.send(f"{ctx.author.mention}, You need to submit a valid link!")
            return

    await ctx.send(f"{ctx.author.mention}, Please enter the name of the role you are applying for:")

    def check(m):
        return m.author == ctx.author

    try:
        role_message = await ctx.bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, You did not reply in time. Please try submitting again. Use ``>>submit list`` for a list of available roles")
        return

    if role_message.content.lower() not in [role.lower() for role in roles]:
        await ctx.send(f"{ctx.author.mention}, The specified role does not exist. Please use a valid role. (You must redo the command)\nUse ``>>submit list`` for a list of available roles")
        return

    target_channel = ctx.bot.get_channel(1174282743434186752)
    if not target_channel:
        await ctx.send(f"{ctx.author.mention}, Failed to find the target channel.")
        return
    print(len(dup.attachments))
    try:
        if dup.attachments:
            fat = [] 
            for atta in dup.attachments:
                fat.append(await atta.to_file())
            await target_channel.send(f"Submission from {ctx.author.mention} for role: {role_message.content} with PID: `{PlayerID}`", files=fat[:10])
            if False:
                for attachmenti in range(len(dup.attachments)):
                    i = attachmenti + 1
                    print(attachmenti)
                    fili = dup.attachments[attachmenti]
                    
                    await target_channel.send(f"Submission from {ctx.author.mention} for role: {role_message.content} with PID: `{PlayerID}`\n**This is Image #{i} of {len(dup.attachments)}** (Sorry that it's a file, it's a quickfix since I can't dev rn)\n{fili}")
        elif link:
            await target_channel.send(f"Submission from {ctx.author.mention} for role: {role_message.content} with PID: `{PlayerID}`\n{link}")
        await ctx.send(f"{ctx.author.mention}, Your submission has been successfully sent.")
        if ctx.guild:
            await role_message.delete()
    except disnake.HTTPException as e:
        await ctx.send(f"Failed to send the submission. Error: {e}")
    if ctx.guild:
        await ctx.message.delete()

    

def setup_command(cog):
    cog.bot.add_command(youllnevergetthewhyachievementuwu)
    return youllnevergetthewhyachievementuwu