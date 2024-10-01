from disnake.ext import commands

@commands.command(name='dmnexus', description="DMs Nexus with the idea!")
async def spamme(ctx, *, stri: str):
    mem = ctx.guild.get_member(776940844728057928)
    await mem.send(f"From: {ctx.author.name} | {ctx.author.id}\n```{stri}```")

def setup_command(cog):
    cog.bot.add_command(spamme)
    return spamme