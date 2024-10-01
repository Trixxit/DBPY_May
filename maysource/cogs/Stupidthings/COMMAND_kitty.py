import requests
import disnake
from disnake.ext import commands
import json
import os
import time

@commands.command(name="kitty", help="Get a random cat fact.")
async def kitty(ctx):
    url = "https://catfact.ninja/fact"
    try:
      response = requests.get(url)

      # Check if the request was successful (status code 200)
      if response.status_code == 200:
        print("Request successful!")
        print("Response content:")
        print(response.text)
        data_dict = response.json()

        # Extract values and store them in variables
        fact = data_dict['fact']
        length = data_dict['length']
        await ctx.send(f"Cat fact: {fact}")
      else:
        print(f"Request failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")


def setup_command(cog):
    cog.bot.add_command(kitty)
    kitty.extras["example"] = "No Example Set"
    return kitty