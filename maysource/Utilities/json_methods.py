import json
import aiofiles
from pathlib import Path

async def read_json(file_path: str) -> dict:
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        data = await file.read()
        return json.loads(data)

async def write_json(file_path: str, data):
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, indent=4))


def rmFindAlg(input_str, reverse_mapping):
    normalized_input = input_str.lower()
    for x in reverse_mapping.keys():
        if x.lower() == normalized_input:
            return x
    for key, aliases in reverse_mapping.items():
        normalized_aliases = [alias.lower() for alias in aliases]
        if normalized_input in normalized_aliases:
            return key
    return None

def maptoJSON(filename):
    curp = Path(__file__).resolve()
    proot = curp.parent.parent
    return f"{proot}/JSONs/{filename}"


def FindkeyCIS(data: dict, search: str):
    def find_key_recursive(current_data, search, parent_keys=[]):
        if isinstance(current_data, dict):
            for key, value in current_data.items():
                if key.lower() == search.lower():
                    return key
                if isinstance(value, dict):
                    result = find_key_recursive(value, search, parent_keys + [key])
                    if result is not None:
                        return result
        return None
    return find_key_recursive(data, search)