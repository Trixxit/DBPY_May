from disnake.ext import commands

roles = {
    1185184571650756658: ["detrusted", "detrust", "nomedia", "media", "noimages", "images", "image", "noimage"],
    1194556618860400701: ["achievement", "achievements"]
}

achis = [
    1194551083578691644,
    1194613154685145151,
    1194613153150009384,
    1194551109876985966,
    1194613146409762847,
    1194614106007814145,
    1194613142488109146,
    1194612933645312070,
    1194578016379093053,
    1194614103382171730,
    1194612848677113856,
    1194613150423711814,
    1194613140202192947,
    1194613144392302643,
    1194613138755174400,
    1189380987977732216,
    1194551074380578861,
    1194614100748152842,
    1194551088376971314,
    1194613156216057907,
    1194613148406259792
]

@commands.command(name='__unblacklist', description="Blacklist a member from something!")
async def allunblacklist(ctx):
    print("Blank command")


def setup_command(cog):
    cog.bot.add_command(allunblacklist)
    allunblacklist.extras["example"] = "No Example Set"
    return allunblacklist