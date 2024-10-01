import json
import disnake
from disnake.ext import commands
from Utilities.discord_utils import create_embed, randcolor
from Utilities.staffchecks import Anystaffcheck
import asyncio
def load_database():
    with open('database.json', 'r') as f:
        return json.load(f)

def save_database(database):
    with open('database.json', 'w') as f:
        json.dump(database, f, indent=4)


@commands.command(name="addquestion", description="Add a question and answer to the database.")
@Anystaffcheck((1231831222930636800, 1180945644567941272))
async def addquestion(ctx, *, question):
    await ctx.send(f"Please provide the answer for the question: {question}")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        answer_msg = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        answer = answer_msg.content

        database = load_database()

        database['q_and_a'].append({"question": question, "answer": answer})

        save_database(database)

        await ctx.send("The question and answer have been added to the database.")

        await ctx.message.delete()
        await answer_msg.delete()

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Please try adding the question again.")

def setup_command(cog):
    cog.bot.add_command(addquestion)
    return addquestion