from Utilities.json_methods import maptoJSON, read_json, write_json
from Utilities.staffchecks import Anystaffcheck, admin, headguide
from disnake.ext import commands

@commands.command(name='jedit', description="Replace a value of the JSON")
@Anystaffcheck((admin, headguide))
async def jedit(ctx, file: str, path: str, val: str):
    try:
        data = await read_json(maptoJSON(file + '.json'))
    except Exception as e:
        print(e)
        await ctx.send(f"Failed to read `{file}.json`")
        return

    if data is None:
        await ctx.send(f"Failed to read `{file}.json` or the file was empty.")
        return

    keys = path.split("/")
    current_data = data
    for i, key in enumerate(keys):
        if isinstance(current_data, dict):
            key_lower = key.lower()
            matched_key = next((k for k in current_data if k.lower() == key_lower), None)
            if matched_key is not None:
                if i == len(keys) - 1:
                    # Replace the value at the final key
                    current_data[matched_key] = val
                    break
                current_data = current_data[matched_key]
            else:
                await ctx.send(f"Key '{'/'.join(keys)}' not found in `{file}.json`.")
                return
        else:
            await ctx.send(f"Key '{'/'.join(keys)}' not found in `{file}.json`.")
            return

    # Write the updated data back to the JSON file
    try:
        await write_json(maptoJSON(file + '.json'), data)
        await ctx.send(f"Value at `{file}://{'/'.join(keys)}` successfully updated to `{val}`.")
    except Exception as e:
        print(e)
        await ctx.send("Failed to write the updated data to the JSON file.")
    print("Blank command")


def setup_command(cog):
    cog.bot.add_command(jedit)
    jedit.extras["example"] = "No Example Set"
    return jedit