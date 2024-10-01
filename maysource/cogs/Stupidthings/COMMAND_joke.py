import requests
import disnake
from disnake.ext import commands
import json
import os
import time


@commands.command(name="joke", help="Jokes :)")
async def joke(ctx):
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful!")
            print("Response content:")
            print(response.text)
            joke_data = response.json()

            # Extract values and store them in variables
            joke_type = joke_data['type']
            setup = joke_data['setup']
            punchline = joke_data['punchline']
            joke_id = joke_data['id']
            await ctx.send(f"{setup}")
            time.sleep(2)
            await ctx.send(f"||{punchline}||")
        else:
            print(f"Request failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def setup_command(cog):
    cog.bot.add_command(joke)
    joke.extras["example"] = "No Example Set"
    return joke