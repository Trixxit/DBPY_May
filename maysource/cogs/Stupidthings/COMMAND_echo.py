
import disnake
from disnake.ext import commands
import re

@commands.command(name='echo')
async def echo(ctx, *, message: str):
    sanitized_message = message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
    sanitized_message = sanitized_message.replace(f".", f"\.")
    sanitized_message = sanitized_message.replace(f"/", f"\/")
    sanitized_message = sanitized_message.replace(f"@", f"\@")
    role_mentions = re.findall(r'<@&(\d+)>', sanitized_message)

    for role_id in role_mentions:
        role = ctx.guild.get_role(int(role_id))
        if role:
            sanitized_message = sanitized_message.replace(f"<@&{role_id}>", f"@\u200b{role.name}")
        else:
            sanitized_message = sanitized_message.replace(f"<@&{role_id}>", f"@\u200b{role_id}")

    sanitized_message = sanitized_message.replace("fuck", "f\*ck")
    sanitized_message = sanitized_message.replace("shit", "sh\*t")
    sanitized_message = sanitized_message.replace("bitch", "b\*tch")
    sanitized_message = sanitized_message.replace("slut", "sl\*t")
    sanitized_message = sanitized_message.replace("retard", "r\*tard")
    sanitized_message = sanitized_message.replace("nigger", "n\*gger")
    sanitized_message = sanitized_message.replace("dick", "d\*ck")
    sanitized_message = sanitized_message.replace("cock", "c\*ck")
    sanitized_message = sanitized_message.replace("idiot", "id\*\*t")
    sanitized_message = sanitized_message.replace("cunt", "c\*nt")
    sanitized_message = sanitized_message.replace("sex", "s\*x")

    await ctx.send(sanitized_message)

def setup_command(cog):
    cog.bot.add_command(echo)
    return echo