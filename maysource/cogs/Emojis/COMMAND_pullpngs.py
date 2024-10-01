from disnake.ext import commands
import disnake
import asyncio

from Utilities.staffchecks import staffguideCheck

class EmojiListPaginator:
    def __init__(self, ctx, emojis, page_size=10):
        self.ctx = ctx
        self.emojis = emojis
        self.page_size = page_size
        self.current_page = 0

    async def send_initial_message(self):
        if not self.emojis:
            await self.ctx.send("No emojis found in this server.")
            return

        message = await self.ctx.send(embed=self.create_page_embed())
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
        return message

    def create_page_embed(self):
        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size
        page_emojis = self.emojis[start_index:end_index]

        embed = disnake.Embed(title=f"Server Emojis - Page {self.current_page + 1}", color=disnake.Color.random())
        for emoji in page_emojis:
            embed.add_field(name=str(emoji), value=emoji.url, inline=True)

        return embed

    async def paginate(self, message):
        def check(reaction, user):
            return user == self.ctx.author and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == message.id

        while True:
            try:
                reaction, user = await self.ctx.bot.wait_for('reaction_add', timeout=6000.0, check=check)

                if str(reaction.emoji) == "➡️" and self.current_page < (len(self.emojis) - 1) // self.page_size:
                    self.current_page += 1
                    await message.edit(embed=self.create_page_embed())
                elif str(reaction.emoji) == "⬅️" and self.current_page > 0:
                    self.current_page -= 1
                    await message.edit(embed=self.create_page_embed())

                await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break

@commands.command(name='listemojis', description="Lists all emojis in the server")
@staffguideCheck()
async def listemojis(ctx):
    if not ctx.channel.id in [1193586146450608148, 972408205990821908, 1186393899128852580, 1191889768334774303]:
        return
    all_emojis = [emoji for guild in ctx.bot.guilds for emoji in guild.emojis]
    paginator = EmojiListPaginator(ctx, all_emojis)
    message = await paginator.send_initial_message()
    if message:
        await paginator.paginate(message)


def setup_command(cog):
    cog.bot.add_command(listemojis)
    return listemojis
