import re
import aiofiles
import disnake
from disnake.ext import commands, tasks
import random
import time
import asyncio
import os
import aioschedule
import datetime
from fuzzywuzzy import fuzz
import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from Utilities.discord_utils import sanmes, mprint
from Utilities.staffchecks import admin_roles, user_has_role, staff_roles, staffCheck, all_staff, Anystaffcheck, admin, lcm, cm, mod
from Utilities.json_methods import read_json, write_json, maptoJSON
from Utilities.fake_ip_stuff import randomize_data, random_ip, random_ipv6
import threading
from Utilities.roles import bases, ranks, legendaries, combined_roles
from Utilities.responses import getResponse, CheckFailure, Blacklisted, shouldI, Disabled, BadArgument, Cooldown, MissingArg, NotFound
import traceback
import linecache


isBrained = 0
Braining = 0
MayMimics = []
printLogging = False
Version = "1.4.9"
starttime = time.time()

RikuSummon = False
isError = True
Reactions = True
replymes = None
LeNoBrainFr = []

intents = disnake.Intents.all()
act = disnake.Activity(
    name = " Aaron do stupid things",
    type=disnake.ActivityType.watching,
    url="https://www.youtube.com/watch?v=BXiQEwN5Pkk"

)
maybot = commands.Bot(activity = act, owner_ids = (776940844728057928, 1137611032311902299), command_prefix=[">>", ".may ", ".May "], intents=intents, status="``.May`` -- Currently in dev! Message <@776940844728057928>", help_command=None, case_insensitive=True)

yoms_revenge = {}
yoms_anger = False
once_done = False

@maybot.event
async def on_ready():
    if not once_done:
        for folder in os.listdir('/home/container/maysource/cogs'):
            if os.path.exists(os.path.join('/home/container/maysource/cogs', folder, '__init__.py')):
                maybot.load_extension(f'cogs.{folder}')

        category = maybot.get_channel(1187139289163776010)
        if category:
            for channel in category.channels:
                yoms_revenge[channel.id] = channel.position

        word_count = 0
        number_of_functions = sum(hasattr(attr, '__call__') for attr in globals().values())
        current_time = time.time()
        load_time = current_time - starttime
        script_name = 'main.py'
        channel_count = sum(1 for _ in maybot.get_all_channels())
        strig = "Guilds:"
        for x in maybot.guilds:
            strig += f"\n{x.name} : {x.id}"
        mprint(f'Logged in as {maybot.user.name}')
        mprint(f'ID: {maybot.user.id}')
        mprint(f'Guilds: {len(maybot.guilds)}')
        mprint(strig)
        mprint(f'Users: {len(maybot.users)}')
        mprint(f'Channels: {channel_count}')
        mprint(f"Ready time: {load_time:.3f} seconds")
        mprint(f"Methods Loaded: {number_of_functions}")
        mprint(f"Commands attached: {len(maybot.commands)}")
        try:
            with open(script_name, 'r', encoding='utf-8') as file:
                content = file.read()
                words = content.split()
                word_count = len(words)
                mprint(f"Total file size: {word_count} words")
        except FileNotFoundError:
            mprint(f"File {script_name} not found.")
        mprint(f"Bot Name: {maybot.user.name}")
        mprint(f"Bot ID: {maybot.user.id}")
        channel = maybot.get_channel(972408205990821908)
        if channel:
            if printLogging:
                await channel.send("Loading...")
                await asyncio.sleep(3)
                await channel.send("-- ONREADY COMPILED -- ")
                await channel.send(f'Guilds: {len(maybot.guilds)}')
                await channel.send(f'Users: {len(maybot.users)}')
                await channel.send(f'Channels: {channel_count}')
                await channel.send(f"Ready time: {load_time:.3f} seconds")
                await channel.send(f"Methods Loaded: {number_of_functions}")
                await channel.send(f"Commands attached: {len(maybot.commands)}")
                await channel.send(f"Bot Version: {Version}")
                await channel.send(f"Main file size: {word_count} words.")
                await channel.send(f"Bot Name: {maybot.user.name}")
                await channel.send(f"Bot ID: {maybot.user.id}")
                await channel.send("May hath been awakened.")

        threading.Thread(target=input_loop, daemon=True).start()
        yomling_attacks.start()
        mprint(f"--- ONREADY COMPLETE ---")
        mprint("Hello Everyone!")

@tasks.loop(minutes=60)
async def yomling_attacks():
    data = await read_json(maptoJSON("rolestuff.json"))
    datad = data
    usersd = []
    for users in data["customrolestuff"]:
        role_data = data["customrolestuff"][users]
        expiry_date = role_data["expiry"]
        current_time = datetime.datetime.now()
        if datetime.datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M:%S.%f') < current_time:
            guild = maybot.get_guild(971700371112198194)
            role = guild.get_role(role_data["id"])
            if role == None:
                usersd.append(users)
            else:
                usersd.append(users)
                await role.delete()
    
    for i in usersd:
        del datad["customrolestuff"][i]

    mprint("Yomling strikes!")
    deathtime = datetime.datetime.now()
    the_executed = await yoms_victims()
    whose_who_remain_dead = {}
    await write_json(maptoJSON("rolestuff.json"), datad)
    for forehead_barcode, raw_resurrection_date in the_executed.items():
        resurrection_date = datetime.datetime.fromisoformat(raw_resurrection_date)
        if deathtime >= resurrection_date:
            grave = maybot.get_guild(971700371112198194)
            revived = grave.get_member(int(forehead_barcode))
            if revived:
                role = disnake.utils.get(grave.roles, id=1105083101849325678)
                if role:
                    await revived.remove_roles(role)
                    mprint(revived.display_name + " has been revived!")
                    try:
                        await revived.send("You've been ~~released from account age purgatory~~ unmuted in Soul Knight Prequel as your account is now 30 days old!")
                    except:
                        pass
        else:
            whose_who_remain_dead[forehead_barcode] = raw_resurrection_date
    await resume_purgatory(whose_who_remain_dead)

async def yoms_victims():
    mprint("Getting Victims...")
    return await read_json(maptoJSON("stuff.json"))

async def resume_purgatory(the_dead_speak_no_words):
    mprint("Saving victims...")
    await write_json(maptoJSON("stuff.json"), the_dead_speak_no_words)

@maybot.event
async def on_member_join(member):
    mprint("Member joined!")
    officer_I_swear_she_said_she_was_30 = (datetime.datetime.now(datetime.timezone.utc) - member.created_at).days
    mprint("Age: " + str(officer_I_swear_she_said_she_was_30))
    if officer_I_swear_she_said_she_was_30 < 30:
        mprint("Member is under 30")
        unsafe_unsavoury_activity = disnake.utils.get(member.guild.roles, id=1105083101849325678)
        if unsafe_unsavoury_activity:
            mprint("Gave role")
            await member.add_roles(unsafe_unsavoury_activity)
            thine_abyssal_residents = await yoms_victims()
            freedom_is_but_a_dream = datetime.datetime.now() + datetime.timedelta(days=30)
            thine_abyssal_residents[str(member.id)] = freedom_is_but_a_dream.isoformat()
            await resume_purgatory(thine_abyssal_residents)
            await member.send(f"You have been muted for 30days for our server's protection due to your account's circumstances. Please make a ticket <#1176532007837249567> if you have a different issue not relating to this action, or by DMing a moderator.\nThanks!")
            mprint("complete")
def save_role_database(role_data):
    with open('roles.json', 'w') as f:
        json.dump(role_data, f, indent=4)

def load_role_database():
    try:
        with open('roles.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

role_data = load_role_database()
        
@maybot.event
async def on_raw_member_update(member):
        role_data[str(member.id)] = [role.id for role in member.roles if role.name != "@everyone" and role.id not in [1243408241136767067, 971704489520300032, 971704808593559562, 1231831222930636800, 1198083342990581780, 1186624610469421076, 971704672278675456, 1180945644567941272, 1196465778438963392, 1183808147568210050, 1178888662465917031, 1180235184747057162, 1191893059970011276, 1191892769535443046, 1196761863002787971, 1087662750743932978]]
        #print(role_data)
        save_role_database(role_data)

@maybot.event
async def on_member_join(member):
    # Reassign the roles to the member who joined
    if str(member.id) in role_data:
        roles_to_add = [disnake.Object(id=role_id) for role_id in role_data[str(member.id)] if role_id not in [1243408241136767067, 971704489520300032, 971704808593559562, 1231831222930636800, 1198083342990581780, 1186624610469421076, 971704672278675456, 1180945644567941272, 1196465778438963392, 1183808147568210050, 1178888662465917031, 1180235184747057162, 1191893059970011276, 1191892769535443046, 1196761863002787971, 1087662750743932978]]
        await member.add_roles(*roles_to_add)
        #print(roles_to_add)
        del role_data[str(member.id)]  # Remove entry after roles are reassigned
        save_role_database(role_data)

@maybot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        embed = disnake.Embed(title=f"{before.author.display_name} ({before.author.name}) edited a message with id {before.id} at {before.jump_url} in {before.channel}:", description=f"Message *(Unedited)*:\n{sanmes(before.content)}\n\nMessage *(Edited)*: \n{sanmes(after.content)}")
        await before.channel.guild.get_channel(1250279539360403477).send(embed=embed)

@maybot.event
async def on_message_delete(message):
    embed = disnake.Embed(title=f"{message.author.display_name} ({message.author.name}) deleted a message with id {message.id} at {message.jump_url} in {message.channel}:", description=f"Message: \n{sanmes(message.content)}")
    await message.channel.guild.get_channel(1250279539360403477).send(embed=embed)

def input_loop():
    global replymes
    channel_id = 972408205990821908
    mes_id = 0
    while True:
        inp = input("Waiting for command...")
        inp.replace("kannasip", "<a:kannasip:1190866081322123284>").replace("maybored", "<a:maybored:1190867177067253761>").replace("mayknife", "<:mayknife:1190867171346239578>").replace("maygetout", "<:maygetout:1190867165302235227>").replace("maydead", "<:maydead:1190867158897532938>").replace("maygun", "<:maygun:1190867153432346705>")
        if inp.lower().startswith("--channel:"):
            try:
                new_channel_id = int(inp.lower().replace("--channel:", ""))
                channel_id = new_channel_id
            except Exception as e:
                mprint(f"Error: {e}")
            else:
                mprint(f"Channel switched to {channel_id}")
        elif inp.lower().startswith("--re:"):
            try:
                mes_id = int(inp.lower().replace("--re:", ""))
            except Exception as e:
                mprint(f"Error: {e}")
            else:
                channel = maybot.get_channel(channel_id)
                if channel:
                    try:
                        replymes = channel.fetch_message(mes_id)
                    except:
                        mprint("Failed getting replay message")
                    else:
                        mprint(f"Reply switched to {mes_id}")
                else:
                    mprint("Failed getting channel object")

        else:
            asyncio.run_coroutine_threadsafe(send_message(channel_id, inp), maybot.loop)


async def send_message(channel_id, message):
    global replymes
    channel = maybot.get_channel(channel_id)
    if channel:
        if replymes:
            await replymes.reply(message, mention_author=True)
            replymes = None
        else:
            await channel.send(message)


@maybot.event
async def on_guild_channel_update(before, after):
    if False:
        global yoms_anger, yoms_revenge
        if yoms_anger:
            return

        if after.category_id == 1187139289163776010:
            if before.position != after.position:
                yoms_anger = True
                try:
                    await after.edit(position=yoms_revenge[after.id])
                except disnake.HTTPException as e:
                    mprint(f"Failed to move channel: {e}")
                yoms_anger = False

@maybot.event
async def on_message(message):

    await maybot.process_commands(message)
    global isBrained
    global RikuSummon
    global isBrokey
    cn = message.content.lower()

    if not any([message.author.bot, message.content.startswith(">>")]):
        with open("mayspeak.json", "r") as read_file:
                maydata = json.load(read_file)
        listens = [int(i) for i in maydata.keys()]
        if message.channel.id in listens:
            sender = message.guild.get_channel(int(maydata[str(message.channel.id)]))
            await sender.send(message.content)
    if message.channel.id == 1186393899128852580:
            origin = message.guild.get_channel(1186393899128852580)
            guild = maybot.get_guild(1196678452565266482)
            channel = guild.get_channel(1256156363692703776)
            webhooked = await channel.webhooks()
            for w in webhooked:
                if w.name == "MayWebhook":
                    await w.delete()
            webhook = await channel.create_webhook(name='MayWebhook')
            user_display_name = f"Soulknight Prequel | {origin.name} | {message.author.display_name}"
            try:
                avatar_urled = message.author.guild_avatar.url
            except:
                avatar_urled = message.author.avatar.url
            
            await webhook.send(
                content=sanmes(message.content),
                username=user_display_name,
                avatar_url=avatar_urled
            )
            await webhook.delete()



    if message.author == maybot.user:
        return

    
        
        
    
    if message.author.id == 1027825128324734996333333: #175931110432178176:
        custom_emoji_id = 1192318053057314947
        custom_emoji = maybot.get_emoji(custom_emoji_id)

        if custom_emoji:
            await message.add_reaction(custom_emoji)

    try:
        member = message.guild.get_member(message.author.id)
        if member and user_has_role(member, (1189443616314241034, 1)):
            return
    except:
        pass

    if not message.guild and not message.content.startswith(">>"):
        mprint(f"___DM___ from {message.author.name} | {message.author.id}: {sanmes(message.content)}")
        try:
            mem = maybot.get_channel(1211187631346552872)
            if mem:
                await mem.send(f"___DM___ from {message.author.name} | {message.author.id}: {sanmes(message.content)}")
        except:
            return
    member = None
    if message.guild:
        member = message.guild.get_member(message.author.id)
    if member != None:
        # Staff Message Triggers
        if member != None and user_has_role(member, staff_roles):
            if "may" in message.content.lower() and "murder" in message.content.lower():
                await message.channel.send("Yes sir, an Exoatmospheric kill vehicle is en route as we speak.")
            elif "may" in cn and " ip" in cn:
                await message.channel.send(f"Their IP is: {random_ip()} with an IPv6 of {random_ipv6()}")
            elif (message.content.lower().startswith("may, get ") or message.content.lower().startswith("may get ")) and message.content.lower().endswith(" data"):
                isError = False
                split_message = message.content.split(' ')
                some_text = ' '.join(split_message[2:-1])
                await message.channel.send(f"Collecting {some_text}'s data...")
                await asyncio.sleep(random.randint(5, 10))

                randomized_data = randomize_data()
                await message.channel.send(f"Compiled {some_text}'s data:\n {randomized_data}")
            elif message.channel.id == Braining and isBrained != 0 and (message.content.lower().startswith("may") == False) and (message.content.lower().startswith(">>") == False):
                channel = message.guild.get_channel(isBrained)
                if message.content.lower().startswith("[r:"):
                    mid = None
                    try:
                        mid = int(message.content[3:22])
                    except:
                        await message.channel.send("Failed to parse message id")
                        mprint(message.content[3:22])
                        return
                    mes = None
                    try:
                        mes = await channel.fetch_message(mid)
                    except disnake.NotFound:
                        await message.channel.send("Message not found")
                    except disnake.Forbidden:
                        await message.channel.send("I don't have permissions to see that message.")
                    except disnake.HTTPException as e:
                        await message.channel.send(f"Failed to fetch message")
                        mprint(e)
                    else:
                        await mes.reply((message.content[23:]), mention_author=True)
                else:
                    await channel.send(message.content)

        if message.channel.id != 972061720208105514 and Reactions: #SKPd1
            try:
                if message.channel.id == 972061792966676530: # Announcements
                    await message.add_reaction(maybot.get_emoji(975698551373959199))
                    await message.add_reaction(maybot.get_emoji(975699132939403264))
                    await message.add_reaction(maybot.get_emoji(975698978425413643))
                elif message.channel.id == 972408596707033108: # YT Notif
                    await message.add_reaction(maybot.get_emoji(975698551373959199))
                    await message.add_reaction(maybot.get_emoji(975699132939403264))
                    await message.add_reaction(maybot.get_emoji(975698978425413643))
                elif message.channel.id == 972442301760684082: # Clips Highlights
                    if (not "http" in message.content) and (not message.attachments):
                        await message.delete()
                        return
                    await message.add_reaction("🔥")
                elif message.channel.id == 1175961612855820358: # Clips Highlights
                    if (not "http" in message.content) and (not message.attachments):
                        await message.delete()
                        return
                    await message.add_reaction("🔥")
                elif message.channel.id == 1186653853026889769: # Showcase
                    await message.add_reaction("⬆️")
                    await message.add_reaction("⬇️")
                elif message.channel.id == 972389085136171018: # Fan Art
                    await message.add_reaction("❤️")
                elif message.channel.id == 1185686269397831812: # NonSKP Art
                    await message.add_reaction("❤️")
                elif message.channel.id == 1197866683977707531 or message.channel.id == 1197866986009526363:
                    await message.add_reaction("⬆️")
                    await message.add_reaction("⬇️")
            except:
                mprint("error in reacting")
        if message.author.id == 306770167298392065 and (message.channel.id == 972408205990821908 or message.channel.id == 1179551792959328297) and RikuSummon:
            message.channel.send("Riku summoned successfully")
            RikuSummon = False
        if ((cn.startswith("may") and "may " in cn or "may, " in cn or "may." in cn or "may?" in cn) or (" may" in cn or " may, " in cn or " may." in cn or " may?" in cn)) and "should" in cn:
            if message.channel.category.id == 971701323269554197 or message.channel.id == 972061720208105514 or message.channel.id == 1180473776505360485:
                return
            await message.channel.send(f"{random.choice(shouldI)}")

        try:
            member_roles_ids = {role.id for role in message.author.roles}
            common_base_roles = member_roles_ids.intersection(bases)
            common_rank_roles = member_roles_ids.intersection(ranks)
            elite_heroic_legendary_roles = legendaries

            highest_priority_base = None
            highest_priority_rank = None

            if common_base_roles:
                highest_priority_base = max(common_base_roles, key=lambda x: list(bases).index(x))

            if common_rank_roles:
                highest_priority_rank = max(common_rank_roles, key=lambda x: list(ranks).index(x))

            roles_to_remove = set()

            roles_to_remove.update(common_base_roles - {highest_priority_base} if highest_priority_base else set())
            roles_to_remove.update(common_rank_roles - {highest_priority_rank} if highest_priority_rank else set())

            if not common_base_roles:
                combined_roles_to_remove = set()
                for base_rank_combo, combined_role_id in combined_roles.items():
                    if combined_role_id in member_roles_ids:
                        combined_roles_to_remove.add(combined_role_id)
                roles_to_remove.update(combined_roles_to_remove)


            if highest_priority_base and highest_priority_rank:
                combined_role_id = combined_roles.get((highest_priority_base, highest_priority_rank))
                if combined_role_id:
                    if combined_role_id not in member_roles_ids:
                        combined_role = message.guild.get_role(combined_role_id)
                        await message.author.add_roles(combined_role, reason="Combined role auto-assign")
                    roles_to_remove.update(elite_heroic_legendary_roles - {combined_role_id})

            roles_to_remove = {message.guild.get_role(role_id) for role_id in roles_to_remove if role_id in member_roles_ids}
            if roles_to_remove:
                await message.author.remove_roles(*roles_to_remove, reason="Role auto-adjustment")
        except Exception as e:
            mprint(f"An error occurred in on_message: {e}")
        if ("season" in cn or "seasonal" in cn) and ("delete" in cn or "character" in cn or "useless" in cn or "wipe" in cn or "reset" in cn) and False:
            await message.channel.send("## Your characters will not be wiped between seasons.\n### Read the message by <@204255221017214977>.")
        if "cookie" in cn:
            if random.randint(1, 7) == 2 and not user_has_role(member, staff_roles):
                await message.channel.send("*Steals the cookie*")
        if message.channel.id == 1188839089009590322 or message.channel.id == 972061792966676530 or message.channel.id == 972408596707033108:
            ids = [975698551373959199, 975699132939403264, 975698978425413643]
            for emoji_id in ids:
                emoji = disnake.utils.get(message.guild.emojis, id=emoji_id)
                if emoji:
                    try:
                        await message.add_reaction(emoji)
                    except disnake.HTTPException:
                        mprint(f"Failed to add reaction: {emoji}")
                else:
                    mprint(f"Emoji with ID {emoji_id} not found.")

@maybot.command(name='ping', description="Pong!")
async def ping(ctx):
    await ctx.send(f'Pong! {round(maybot.latency * 1000)}ms')
    cmd = maybot.get_command("ping")




@maybot.event
async def on_command_error(ctx, error):
    senderrormessage = True
    global isError
    if isError == False:
        isError = True
    else:
        if isinstance(error, commands.CheckFailure):
            await ctx.send(getResponse(CheckFailure))
            senderrormessage = False
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(getResponse(NotFound))
            senderrormessage = False
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(getResponse(MissingArg))
            senderrormessage = False
            await ctx.send(f"The missing arguement in question: `{error.param.name}`")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(getResponse(Cooldown))
            await ctx.send(f"Please try again after `{error.retry_after:.2f}` seconds")
            senderrormessage = False
        elif isinstance(error, commands.BadArgument):
            await ctx.send(getResponse(BadArgument))
            senderrormessage = False
        elif isinstance(error, commands.CommandError):
            await ctx.send("The command execution failed, <@996395908654694430> notified")
            mprint(error)
        else:
            mprint(f"An error occurred: {str(error)}")
            await ctx.send("An unexpected error occurred, <@996395908654694430> notified, please try again later!")
        if senderrormessage:
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            error_info = ''.join(tb)
            fullstring = f"An unexpected error occurred in {ctx.channel.mention if ctx.guild else 'DMs'} by {ctx.author.mention} with message {ctx.message.content}:\n```py\n{error_info}\n```"
            filepath, linenumber = extract_error_line(error_info)
            if not filepath or not linenumber:
                fullstring += "Failed to get filepath or line number."
            else:
                context = 4
                content = await get_surrounding_lines_async(filepath, int(linenumber), context)
                fullstring += f"\n- From `{filepath}`, Context (Surrounding {context} lines):\n```py\n{content}\n```"

            me = maybot.get_channel(1211187631346552872)
            if me:
                try:
                    await me.send(fullstring)
                except:
                    mprint(fullstring)

async def get_surrounding_lines_async(filename, line_no, context=2):
    start_line = max(1, line_no - context)
    end_line = line_no + context
    mprint(f"{context} : {start_line} : {end_line} : {line_no}")
    lines = []
    async with aiofiles.open(filename, 'r') as file:
        all_lines = await file.readlines()
        for i, line in enumerate(all_lines[start_line-1:end_line]):
            lines.append(f"{i + start_line}: {line.rstrip()}")

    return '\n'.join(lines)

def extract_error_line(text):
    pattern = r'File "home\\container\\maysource\\([^"]+)", line (\d+), in error'
    match = re.search(pattern, text)

    if match:
        file_path = match.group(1)
        line_number = match.group(2)
        return file_path, line_number
    else:
        return None, None

@maybot.after_invoke
async def after_any_command(ctx):
    mprint(f"------ EXITING COMMAND {ctx.command.name} ------")

@maybot.before_invoke
async def before_any_command(ctx):
    mprint(f"------ ENTERING COMMAND {ctx.command.name} ------")
    mprint(f"--- Message: {ctx.message.content} ---")
    mprint(f"--- AUTHOR: {ctx.author.name} | {ctx.author.id} ---")
    if ctx.guild:
        mprint(f"--- LOCATION: {ctx.channel.name} | {ctx.channel.id} | {ctx.channel.guild.name} ---")
        restricted_role = ctx.guild.get_role(1189443616314241034)
        if restricted_role in ctx.author.roles:
            await ctx.send(getResponse(Blacklisted))
            raise commands.CommandError("User has restricted role.")
    else:
        mprint(f"--- LOCATION: {ctx.author.id} ---")
    

@maybot.command(name="relinkhlc", description="Emergancy relinking of the HLC Cog.")
@commands.is_owner()
async def rlhlc(ctx):
    name = "HotLoading"
    try:
        maybot.unload_extension(f'cogs.{name}')
    except:
        await ctx.send(f"Failed to Unload {name}")
    try:
        maybot.load_extension(f'cogs.{name}')
        await ctx.send(f'Extension `{name}` reloaded.')
    except Exception as e:
        await ctx.send(f'Error occurred: {e}')

@maybot.event
async def on_member_update(before, after):
    global LeNoBrainFr
    try:
        if before.roles != after.roles and False:
            if after.id not in LeNoBrainFr:
                LeNoBrainFr.append(after.id)
            else:
                LeNoBrainFr.remove(after.id)
                return
            member_roles = set(role.id for role in after.roles)
            common_base_roles = member_roles.intersection(bases)
            common_rank_roles = member_roles.intersection(ranks)

            if len(common_base_roles) > 1:
                highest_priority_role = max(common_base_roles, key=lambda x: list(bases).index(x))
                roles_to_remove_ids = common_base_roles - {highest_priority_role}
                roles_to_remove = [after.guild.get_role(role_id) for role_id in roles_to_remove_ids]
                await after.remove_roles(*roles_to_remove, reason="Base role auto-adjustment")
            if len(common_rank_roles) > 1:
                highest_priority_role = max(common_rank_roles, key=lambda x: list(bases).index(x))
                roles_to_remove_ids = common_rank_roles - {highest_priority_role}
                roles_to_remove = [after.guild.get_role(role_id) for role_id in roles_to_remove_ids]
                await after.remove_roles(*roles_to_remove, reason="Rank role auto-adjustment")
            base_role_id = next(iter(common_base_roles))
            rank_role_id = next(iter(common_rank_roles))
            combined_role_id = combined_roles.get((base_role_id, rank_role_id))

            if combined_role_id:
                crrole = after.guild.get_role(combined_role_id)
                if crrole and crrole not in after.roles:
                    await after.add_roles(crrole, reason="Combined role auto-assign")

                elite_heroic_legendary_roles = set(legendaries)
                roles_to_remove_ids = elite_heroic_legendary_roles - {combined_role_id}
                roles_to_remove = [after.guild.get_role(role_id) for role_id in roles_to_remove_ids if role_id in member_roles]

                await after.remove_roles(*roles_to_remove, reason="Non-matching elite/heroic/legendary roles removal")
    except Exception as e:
        mprint(e)


maybot.run('tokenHasBeenHidden')