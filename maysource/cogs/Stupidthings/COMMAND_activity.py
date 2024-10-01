from disnake.ext import commands
import requests

@commands.command(name="activity", help="Find an activity")
@commands.cooldown(1, 30, commands.BucketType.default)
async def activity(ctx):
    url = "https://www.boredapi.com/api/activity"
    try:
      response = requests.get(url)
      if response.status_code == 200:
        print("Request successful!")
        print("Response content:")
        print(response.text)
        data_dict = response.json()
        activity = data_dict['activity']
        activity_type = data_dict['type']
        participants = data_dict['participants']
        price = data_dict['price']
        link = data_dict['link']
        activity_key = data_dict['key']
        accessibility = data_dict['accessibility']
        if link == "":
          link = "No link"
        await ctx.send(
            f"Activity: {activity}\nType: {activity_type}\nLink: <{link}>\nParticipants: {participants}\nPrice: {price}"
        )
      else:
        print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")
      raise e


def setup_command(cog):
    cog.bot.add_command(activity)
    activity.extras["example"] = "No Example Set"
    return activity