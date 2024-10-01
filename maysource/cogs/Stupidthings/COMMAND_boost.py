from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import requests
import disnake
import json
import random
import time
def save_ads(data):
    if not data:
        data = {}
    with open("ads.json", "w") as write_file:
            json.dump(data, write_file)
    with open("ads.json", "r") as read_file:
            data = json.load(read_file)
    return data

def load_ads():
    try:
        with open("ads.json", "r") as read_file:
            data = json.load(read_file)
    except FileNotFoundError:
        data = save_data()

    return data
    


@commands.command(name="ad", help="Ads!")
@commands.cooldown(1, 120, commands.BucketType.default)
@Anystaffcheck((1196761863002787971, 1231831222930636800))
async def ad(ctx):
    ads = load_ads()
    adsname = []
    for r in ads.keys():
        adsname.append(r)
    
    ad = random.choice(adsname)
    addata = ads[ad]
    embeder = []
    if ad == "Boost":
        roles = await ctx.guild.fetch_roles()
        members = []
        for r in roles:
            if r.is_premium_subscriber():
                members = r.members
        membersnames = [str("`")+t.display_name+str("`") for t in members]
        l = "\n".join(membersnames)
        embed = disnake.Embed(title=f"Thank you!", description=f"A huge thanks to our boosters who have boosted the server, allowing us access to so many emojis and sticker slots!\n{l}\nOnce again, we are thankful for the boost and hope you will continue boosting us in the future! \:)")
        embeder.append(embed)
    else:
        Imgs = addata.get("Imgs","")
       
        if Imgs != None:
            for keyed in Imgs:
                embede = disnake.Embed(title=f"{addata.get('Title', 'No Title')}", description=f"{addata.get('Description', 'No Description')}", url=ctx.channel.jump_url)
                embede.set_image(url=Imgs[keyed])
                embeder.append(embede)
        else:
            embed = disnake.Embed(title=f"{addata.get('Title', 'No Title')}", description=f"{addata.get('Description', 'No Description')}", url=ctx.channel.jump_url)
            embeder.append(embed)
        

    channel = ctx.channel
    webhook = await channel.create_webhook(name='MayWebhook')
    await ctx.message.delete()

    await webhook.send(
        embeds = embeder,
        username="Gloria",
        avatar_url="https://cdn.discordapp.com/emojis/1195000331814326342.png"
    )
    await webhook.delete()



def setup_command(cog):
    cog.bot.add_command(ad)
    ad.extras["example"] = "No Example Set"
    return ad