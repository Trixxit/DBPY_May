import disnake
from disnake.ext import commands
import requests
import asyncio
import time
    

    

@commands.command(name="fortune", help="Fortune favours the bold, but I favour you ~ Entity <3")
async def fortune(ctx):
    
        api_url = "https://fortune-cookie4.p.rapidapi.com/"
        headers = {
            "X-RapidAPI-Key": "07be49fb7amsh80a966fd5d5a907p116280jsnc412cd253843",
            "X-RapidAPI-Host": "fortune-cookie4.p.rapidapi.com"
        }
        last_request_time = 0
        async def send_fortune_cookie_message(ctx):
            fortune_cookie_data = await fetch_fortune_cookie()
            if fortune_cookie_data and len(fortune_cookie_data) > 0:
                message = fortune_cookie_data['data']['message']
            else:
                message = "Future too cloudy"
            channel = ctx.channel
            webhook = await channel.create_webhook(name='MayWebhook')
            await webhook.send(
                content=f"🔮{message}🔮",
                username="Scryer",
                avatar_url="https://cdn.discordapp.com/attachments/972408205990821908/1232349273912508577/Screenshot_20240324-235250.png?ex=66292232&is=6627d0b2&hm=5424ab3ebd85857a1c18e7d987a4cf4eff2fc81c39248ae9a8fafc3a45fd7a0a&"
            )
            await webhook.delete()
        async def fetch_fortune_cookie():
            response = requests.get(api_url, headers=headers)
            return response.json()
        current_time = time.time()
        if current_time - last_request_time < 30:
            channel = ctx.channel
            webhook = await channel.create_webhook(name='MayWebhook')
            await webhook.send(
                content=f"Wait, let me clean my glass ball first, {ctx.author.display_name}...",
                username="Scryer",
                avatar_url="https://cdn.discordapp.com/attachments/972408205990821908/1232349273912508577/Screenshot_20240324-235250.png?ex=66292232&is=6627d0b2&hm=5424ab3ebd85857a1c18e7d987a4cf4eff2fc81c39248ae9a8fafc3a45fd7a0a&"
            )
            await webhook.delete()
        else:
            await send_fortune_cookie_message(ctx)
            last_request_time = current_time


def setup_command(cog):
    cog.bot.add_command(fortune)
    fortune.extras["example"] = "No Example Set"
    return fortune