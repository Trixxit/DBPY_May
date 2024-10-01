from disnake.ext import commands
from markupsafe import escape_silent
from numpy import isin
from Utilities.discord_utils import sendfile
from Utilities.json_methods import maptoJSON, read_json

from Utilities.staffchecks import Anystaffcheck, admin, headguide


@commands.command(name='valueof', description="Returns the value of key at the path of the JSON")
@Anystaffcheck((admin, headguide))
async def valueof(ctx, file: str, *, keysthatareseperatedbyslashes):
    unf = False
    keysthatareseperatedbyslashes = keysthatareseperatedbyslashes.lower()
    if " [unformatted]" in keysthatareseperatedbyslashes: 
        unf = True
        keysthatareseperatedbyslashes.replace(" [unformatted]", "")
    try:
        data = await read_json(maptoJSON(file + '.json'))
    except Exception as e:
        print(e)
        await ctx.send(f"Failed to read `{file}.json`")
        return

    if data is None:
        await ctx.send(f"Failed to read `{file}.json` or the file was empty.")
        return

    keys = keysthatareseperatedbyslashes.split("/")
    current_data = data
    for key in keys:
        if isinstance(current_data, dict):
            key_lower = key.lower()
            matched_key = next((k for k in current_data if k.lower() == key_lower), None)
            if matched_key is not None:
                current_data = current_data[matched_key]
            else:
                await ctx.send(f"Key '{'/'.join(keys)}' not found in `{file}.json`.")
                return
        else:
            await ctx.send(f"Key '{'/'.join(keys)}' not found in `{file}.json`.")
            return

    if current_data:
        if isinstance(current_data, dict) and not unf:
            strig = ""
            for x, y in current_data.items():
                if isinstance(y, str):
                    y = '"' + y + '"'
                if isinstance(x, str):
                    x = f'"{x}"'
                strig += f"\n{x} :\n{y}"
            current_data = strig
        
        if len(current_data) < 1900:
            await ctx.send(f"Value of `{file}://{'/'.join(keys)}`: ```json{current_data}\n```")
        else:
            await sendfile(current_data, ctx, message=f"Value of `{file}://{'/'.join(keys)}`:")

def setup_command(cog):
    cog.bot.add_command(valueof)
    return valueof
