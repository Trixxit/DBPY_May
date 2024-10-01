from disnake.ext import commands
from Utilities.discord_utils import create_embed, randcolor
import random
import disnake

maybot = None

Season0 = "[1](https://media.discordapp.net/attachments/1180235360215765022/1185622329531834378/BossTimeSpawnV2.png?ex=65998257&is=65870d57&hm=cba665814413b84a685fdfbdf0063f7ad8ca4b9a9a1feaea6903fcaa41380146&=&format=webp&quality=lossless&width=567&height=670.png)"
Season1 = "[2](https://imgur.com/gallery/MnGLDtd.png)"

@commands.command(name= "Boss", aliases=["bosses", "timings", "boss time"], description="Shows Boss Timings")
async def Boss(ctx):
    embed = create_embed(title="Boss Timings", description="Timezone independent where you download the app. in.", fields=[{"name":"Note:", "value": "Black Archknight appears on Heroic Difficulty, and you can't cheat your in game time."}], color=randcolor())
    await ctx.send(embed=embed)
    await ctx.send(Season0)
    await ctx.send(Season1)

def setup_command(cog):
    cog.bot.add_command(Boss)
    return Boss