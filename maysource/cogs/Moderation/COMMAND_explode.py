import disnake
from disnake.ext import commands
from Utilities.staffchecks import modcheck, user_has_role, all_staff
import time
import random

maybot = None

@commands.command(name="explode", description="Custom purge command that removes ALL traces of someone in a channel over the past 14 days.") # Declaration
@modcheck() # Check call to another method. Command execution will fail if this check fails
async def explodeballs(ctx, one: str, two: str, three: str, id: int, number: int = 9999): # Definition
    global maybot
    channel = ctx.channel  # Get the channel it was run in
    member = maybot.get_user(id) # Get the member that needs puring
    actual_member = ctx.guild.get_member(id) # Get the ACTUAL member object (the above is a user object)
    if user_has_role(actual_member, all_staff) and member.id != 776940844728057928: # Make sure it can't be used on staff except me
        await ctx.send("Target is staff. Request Denied.") # Send a denial message
    elif member == None: # If the member object wasn't found (invalid id)
        await ctx.send(f"No user with id {id} found") # Send message
    else: # Else, enact the purge
        start = time.time() # Timer for QoL timing
        deleted_count = 0 # Amount of messages deleted
        await ctx.send(f"Found user with id {id}\nBeginning operation...") # Feedback
        if (random.randrange(1, 1000000)) == 42:
            await ctx.send("<@784974333554196511> is exploding!")
        print(f"Found user with id {id}") # Console Feedback
        try: # Wrapped in a try-catch block because discord gives the bot an error if the message's age > 14 days
            async for message in channel.history(limit=None): # Discord API Wrapper (Disnake) method to get every message object in that channel
                if message.author.id == id: # If the message author's id matches the purgee's id
                    await message.delete() # Async operation to remove it
                    deleted_count += 1 # Increment the deleted_count counter
                    if deleted_count == number:
                        end = time.time() # End timer for QoL
                        await ctx.send(f"Removed {deleted_count} messages from <@{id}> in channel {ctx.channel.name} in {end - start} seconds!") # Final EUF
                        return
                    print(f"Removed Message. Total: {deleted_count}") # Console Log
        except Exception as e: # Catch for general exceptions
            await ctx.send("Encountered error and the loop was forced to exit.") # EUF
            print(e) # BEF
        end = time.time() # End timer for QoL
        await ctx.send(f"Removed {deleted_count} messages from <@{id}> in channel {ctx.channel.name} in {end - start} seconds!") # Final EUF

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(explodeballs)
    return explodeballs