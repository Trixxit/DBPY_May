from disnake.ext import commands
import typing
import re
import disnake
import json
from Utilities.discord_utils import create_embed
from Utilities.staffchecks import modevalcheck, staffguideCheck, user_has_role
from Utilities.json_methods import read_json, maptoJSON, write_json
import asyncio

role_mapping = {
    "blessed by rng": 1194551083578691644,
    "why..?": 1194613154685145151,
    "truly insane": 1194613153150009384,
    "insanity": 1194551109876985966,
    "cornucopia": 1194613146409762847,
    "prequelmon master": 1194614106007814145,
    "caught them all": 1194613142488109146,
    "gear loyalist": 1194612933645312070,
    "easter egg hunter": 1194578016379093053,
    "heavenly protection": 1194614103382171730,
    "scaredy cat": 1194551079380189216,
    "extinction": 1194612848677113856,
    "wan piece enthusiast": 1194613150423711814,
    "stamp collector": 1194613140202192947,
    "beginners luck": 1194613144392302643,
    "cant touch this": 1194613138755174400,
    "carnelian": 1259160729714688101,
    "square": 1194614100748152842,
    "apex warrior": 1194551088376971314,
    "rechord": 1194613156216057907,
    "chimera": 1197858877304213504,
    "gladiator": 1197858873663570054,
    "tria": 1197858880349274112,
    "berserker": 1197858883327242290,
    "john wick": 1197858886540083211,
    "fanboy": 1197858859772035132,
    "epic!": 1197858863089717338,
    "huh?!": 1228816169021214760,
    "功夫": 1228815771753517217,
    "prequel of legends": 1228813651876511814,
    "pop culture" : 1228815219678118124
}

@commands.command(name='deny', description="Deny a submission")
@modevalcheck()
async def indenial(ctx, message_link: str, *, role: str):
    def save_data(data):
        datad = {}
        for i in data.keys():
            datad[i] = data[i].id
        print(datad)

        with open("verifyids.json", "w") as write_file:
            json.dump(datad, write_file)
        with open("verifyids.json", "r") as read_file:
                datak = json.load(read_file)
        print(datak)
        return datad
    
    def load_data():
        try:
            with open("verifyids.json", "r") as read_file:
                data = json.load(read_file)
            datad = {}
            for i in data.keys():
                guild_instance = ctx.bot.get_guild(971700371112198194)  # Get guild instance
                member_data = data[i]
                member_instance = guild_instance.get_member(member_data)  # Get member instance
                datad[int(i)] = member_instance
        except FileNotFoundError:
            datad = {}
            save_data(datad)
        return datad
    mids = load_data()
    
    if ctx.channel.id != 1195177920767991909 and ctx.channel.id != 972408205990821908:
        await ctx.send("Wrong channel! Please use <#1195177920767991909>")
        return

    match = re.search(r'discord\.com/channels/(\d+)/(\d+)/(\d+)', message_link)
    if not match:
        await ctx.send("Invalid message link.")
        return

    guild_id, channel_id, message_id = map(int, match.groups())

    channel = ctx.guild.get_channel(1174282743434186752) # Role subs
    # channel = ctx.guild.get_channel(972408205990821908) # Staff Commands
    # channel = ctx.guild.get_channel(1195177920767991909) # Eval
    if not channel:
        await ctx.send("Channel not found.")
        return

    message = None
    try:
        message = await channel.fetch_message(message_id)
        print(f"Message found: {message.content}")
    except disnake.NotFound:
        await ctx.send("Message not found.")
    except disnake.Forbidden as ef:
        await ctx.send("I don't have permission to access that message.")
        raise ef
    except disnake.HTTPException as e:
        await ctx.send(f"An HTTP exception occurred: {e}")
    if not message:
        return
    
    roleobj = None
    if role.lower() not in role_mapping.keys():
        await ctx.send(f"Role `{role.lower()}` not found")
        return
    roleobj = ctx.guild.get_role(role_mapping[role.lower()])

    if roleobj == None:
        await ctx.send("Role object not found")
        return


    data = await read_json(maptoJSON("achi.json"))
    if message.id in data["Denied"]:
        await ctx.send("This submission has already been denied!")
        return
    
    author = None
    if len(message.mentions) > 0:
        author = message.mentions[0]
    if not author:
        await ctx.send("Failed to parse author.")
        return


    data["Denied"].append(message.id)
    if message.id in mids.keys():
        del mids[message.id]
    await write_json(maptoJSON("achi.json"), data)
    await ctx.send("Insert denial reason. Send ``none`` for no reason, send ``pid`` for the preset PID response, send ``invalid`` for the default invalid submission response.")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    reason = None
    reasonmsg = None
    try:
        reasonmsg = await ctx.bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.send("No reply detected, submitting with no reason.")
        return
    if not reasonmsg:
        reason = None
    else:
        reason = reasonmsg.content
    if reason.lower() == "none" or reason.lower() == "no" or reason.lower() == "no reason":
        reason = None
    elif reason.lower() == "pid":
        reason = "Your submission is either missing a PID, the PID was unclear / hard to read, or the PID did not match the one you have bound to your account!"
    elif reason.lower() == "invalid":
        reason = "Your submission did not fufill the critera for the specified role."
    await ctx.send(f"{message_link} by {author.mention} has been denied by `{ctx.author.name}` (`{ctx.author.id}`) from the submission {message_link} with {('The reason: `' + reason + '`') if reason != None else 'No reason'}")
    embed = create_embed(title="Invalid Submission!", description=f"Your submission for the `{roleobj.name}` achievement was denied. {'' if reason == None else ('**Reason:** ' + reason)}", color=disnake.Colour.dark_red())

    await message.add_reaction("❌")
    
    await author.send(embed=embed)
    save_data(mids)

def setup_command(cog):
    cog.bot.add_command(indenial)
    return indenial