from disnake.ext import commands
import typing
import re
import disnake
from Utilities.discord_utils import create_embed
from Utilities.staffchecks import modevalcheck, user_has_role
from Utilities.json_methods import read_json, maptoJSON
import json


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

@commands.command(name='verify', description="Verifies a submission and grants a role")
@modevalcheck()
async def verify(ctx, message_link: str, *, role: typing.Union[str, int]):
    
    def save_data(data):
        datad = {}
        for i in data.keys():
            if data[i] is not None:  # Check if the member instance is not None
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
                if member_instance is not None:  # Check if member_instance is valid
                    datad[int(i)] = member_instance
                else:
                    print(f"Member with ID {member_data} not found in guild.")
        except FileNotFoundError:
            datad = {}
            save_data(datad)
        return datad

    mids = load_data()
    save_data(mids)
    
    if ctx.channel.id not in {1195177920767991909, 972408205990821908}:
        await ctx.send("Wrong channel! Please use <#1195177920767991909>")
        return

    match = re.search(r'discord\.com/channels/(\d+)/(\d+)/(\d+)', message_link)
    if not match:
        await ctx.send("Invalid message link.")
        return

    guild_id, channel_id, message_id = map(int, match.groups())

    channel = ctx.guild.get_channel(1174282743434186752)  # Role subs
    if not channel:
        await ctx.send("Channel not found.")
        return

    try:
        message = await channel.fetch_message(message_id)
        print(f"Message found: {message.content}")
    except disnake.NotFound:
        await ctx.send("Message not found.")
        return
    except disnake.Forbidden as ef:
        await ctx.send("I don't have permission to access that message.")
        raise ef
    except disnake.HTTPException as e:
        await ctx.send(f"An HTTP exception occurred: {e}")
        return
    
    author = message.mentions[0] if message.mentions else None
    if not author:
        await ctx.send("Failed to parse author.")
        return

    if author.id == ctx.author.id:
        await ctx.send("You can't verify yourself!")
        return

    denied_ids = (await read_json(maptoJSON("achi.json")))["Denied"]
    if message.id in denied_ids:
        await ctx.send("This submission has already been denied!")
        return

    if isinstance(role, str):
        roleobj = ctx.guild.get_role(role_mapping.get(role.lower()))
    else:
        roleobj = ctx.guild.get_role(role) if role in role_mapping.values() else None

    if roleobj is None:
        await ctx.send(f"Role `{role}` not found or invalid.")
        return
    
    if user_has_role(author, (roleobj.id,)):
        await ctx.send(f"{author.mention} already has the role {roleobj.name}!")
        return

    if message.id in mids:
        if mids[message.id].id == ctx.author.id:
            await ctx.send(f"You've already verified this, {ctx.author.mention}")
            return
        try:
            await ctx.send(f"{message_link} by {author.mention} has been verified for `{roleobj.name}` (`{roleobj.id}`) by `{ctx.author.name}` (`{ctx.author.id}`) and `{mids[message.id].name}` (`{mids[message.id].id}`)")
            embed = create_embed(title="Congrats!", description=f"Your submission for the `{roleobj.name}` achievement was verified!", color=disnake.Colour.green())
            await author.add_roles(roleobj, reason=f"{message_link} by {author.mention} has been verified for `{roleobj.name}` (`{roleobj.id}`) by `{ctx.author.name}` (`{ctx.author.id}`) and `{mids[message.id].name}` (`{mids[message.id].id}`)")
            mids.pop(message_id)
            await author.send(embed=embed)
            await message.add_reaction("✅")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            raise e
    else:
        await ctx.send(f"{message_link} by {author.mention} has been partially verified for `{roleobj.name}` (`{roleobj.id}`) by `{ctx.author.name}` (`{ctx.author.id}`) and requires a second person for full verification")
        mids[message.id] = ctx.author

    save_data(mids)
    mids = load_data()
    print(mids)

def setup_command(cog):
    cog.bot.add_command(verify)
    return verify
