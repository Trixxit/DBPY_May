from Utilities.json_methods import maptoJSON, read_json, write_json
from Utilities.staffchecks import Anystaffcheck, admin, headguide
from disnake.ext import commands

@commands.command(name='jadd', description="Add a key to a JSON point")
@Anystaffcheck((admin, headguide))
async def jadd(ctx, file: str, path: str, key: str, val: str):
    try:
        data = await read_json(maptoJSON(file + '.json'))
    except Exception as e:
        await ctx.send(f"Failed to read `{file}.json`: {e}")
        return

    if data is None:
        await ctx.send(f"Failed to read `{file}.json` or the file was empty.")
        return

    keys = path.split("/")
    current_data = data
    for i, k in enumerate(keys):
        if isinstance(current_data, dict):
            k_lower = k.lower()
            matched_key = next((kk for kk in current_data if kk.lower() == k_lower), None)
            if matched_key is not None:
                if i == len(keys) - 1:
                    # Add the new key-value pair
                    if key in current_data[matched_key]:
                        await ctx.send(f"Key `{key}` already exists at `{file}://{'/'.join(keys)}`.")
                        return
                    current_data[matched_key][key] = val
                    break
                current_data = current_data[matched_key]
            else:
                await ctx.send(f"Path '{'/'.join(keys)}' not found in `{file}.json`.")
                return
        else:
            await ctx.send(f"Path '{'/'.join(keys)}' leads to a non-dictionary type in `{file}.json`.")
            return

    # Write the updated data back to the JSON file
    try:
        await write_json(maptoJSON(file + '.json'), data)
        await ctx.send(f"Key `{key}` with value `{val}` successfully added to `{file}://{'/'.join(keys)}`.")
    except Exception as e:
        await ctx.send(f"An error occurred while writing the updated data to `{file}.json`: {e}")
    print("Blank command")


def setup_command(cog):
    cog.bot.add_command(jadd)
    jadd.extras["example"] = "No Example Set"
    return jadd