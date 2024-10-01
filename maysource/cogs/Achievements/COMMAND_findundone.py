from disnake.ext import commands
from Utilities.staffchecks import modevalcheck
import disnake
import asyncio


class Paginator:
    def __init__(self, ctx, pages, page=0):
        self.ctx = ctx
        self.pages = pages
        self.page = page
        self.message = None

    async def show_page(self):
        content = '\n'.join(self.pages[self.page])
        if not self.message:
            self.message = await self.ctx.send(content)
            # Add reaction controls
            await self.message.add_reaction("◀️")
            await self.message.add_reaction("▶️")
            self.ctx.bot.loop.create_task(self.wait_for_reaction())
        else:
            await self.message.edit(content=content)

    async def wait_for_reaction(self):
        def check(reaction, user):
            return user == self.ctx.author and str(reaction.emoji) in ["◀️", "▶️"] and reaction.message.id == self.message.id

        while True:
            try:
                reaction, user = await self.ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction.emoji) == "▶️" and self.page < len(self.pages) - 1:
                    self.page += 1
                    await self.message.remove_reaction(reaction, user)
                    await self.show_page()
                elif str(reaction.emoji) == "◀️" and self.page > 0:
                    self.page -= 1
                    await self.message.remove_reaction(reaction, user)
                    await self.show_page()
            except asyncio.TimeoutError:
                try:
                    await self.message.clear_reactions()
                except disnake.Forbidden:
                    pass 
                break


@commands.command(name='findunfinished', description="Prints out a list of message links to submissions that haven't been completed")
@modevalcheck()
async def findundone(ctx):
    channel = ctx.bot.get_channel(1174282743434186752)
    if not channel:
        await ctx.send("Channel not found.")
        return
    limited = 1000
    await ctx.send(f"Searching the most recent `{limited}` messages...")

    messages_with_no_reactions = []
    async for message in channel.history(limit=limited):
        if "Images:" in message.content or "Submission from" in message.content or "https://imgur.com/" in message.content or "https://drive.google.com/file/d/" in message.content or "https://youtu.be/" in message.content or "(Sorry that it's a file, it's a quickfix since I can't dev rn)" in message.content:
          if not "Image" in message.content:
            if len(message.reactions) == 0:
                fix = ""
                print(message.mentions[0].global_name)
                wordlist = message.content.split(" ")
                
                for j in wordlist:
                        if j == "role:":
                            role_check = ""
                            rolecheck = " ".join(wordlist[wordlist.index("role:")+1:wordlist.index("with")]).lower()
                            for c in rolecheck:
                                if str(c).isalnum():
                                    role_check += c
                if ctx.guild.get_member(message.mentions[0].id):
                  for i in ctx.guild.get_member(message.mentions[0].id).roles:
                    role_name = i.name.lower()
                    rolename = ""
                    for c in role_name:
                        if str(c).isalnum():
                            rolename += c
                    print(role_check, rolename)
                    if role_check == rolename:
                        await message.add_reaction("✅")
                        fix = "Role given + No reaction! Adding reaction... "
                    elif role_check == "carnelian" and rolename == "s3carnelian":
                        await message.add_reaction("✅")
                        fix = "Role given + No reaction! Adding reaction... "
                
                
                messages_with_no_reactions.append(f"{fix}[Link](https://discord.com/channels/{ctx.guild.id}/{channel.id}/{message.id})")
                

                
                

    if not messages_with_no_reactions:
        await ctx.send("No messages without reactions found.")
        return

    page_size = 20
    pages = [messages_with_no_reactions[i:i + page_size] for i in range(0, len(messages_with_no_reactions), page_size)]

    paginator = Paginator(ctx, pages)
    await paginator.show_page()

def setup_command(cog):
    cog.bot.add_command(findundone)
    return findundone