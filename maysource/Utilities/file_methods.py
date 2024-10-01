from pathlib import Path
import glob
import os
import disnake
import aiofiles

def getKG() -> str:
    return '`'

def GetProjectPath() -> str:
    curp = Path(__file__).resolve()
    proot = curp.parent.parent
    return str(proot)

    return find_key_recursive(data, search)
    
def count_total_chars(directory):
    file_patterns = ["**/*.json", "**/*.py"]

    total_chars = 0

    for pattern in file_patterns:
        for filepath in glob.glob(os.path.join(directory, pattern), recursive=True):
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                total_chars += len(content)

    return total_chars


def build_tree(directory, ignore=("cache", "vs", "git"), prefix=''):
    items = [item for item in sorted(directory.iterdir()) if not any(ign in item.name.lower() for ign in ignore)]
    tree_str = ""
    for i, item in enumerate(items):
        if i == len(items) - 1:
            joint = "└──"
            extension = "    "
        else:
            joint = "├──"
            extension = "│   "
        
        if item.is_dir():
            tree_str += f"{prefix}{joint} {item.name}/\n"
            tree_str += build_tree(item, ignore, prefix=prefix + extension)
        else:
            tree_str += f"{prefix}{joint} {item.name}\n"
    return tree_str



def FCF(bot, callback_name):
    for command in bot.commands:
        if command.callback.__name__.lower() == callback_name.lower():
            return command.callback.__code__.co_filename
    return None


async def extract_command_code(file_path, callback_name):
    command_start = None
    command_end = None
    command_code = []

    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        lines = await file.readlines()

        for i, line in enumerate(lines):
            if f"async def {callback_name}" in line:
                command_start = i

                for j in range(i, -1, -1):
                    if lines[j].strip().startswith('@commands.command') or lines[j].strip().startswith('@bot.command'):
                        command_start = j
                        break

            if command_start is not None and command_end is None:
                if line.strip() == '' or line.strip().startswith('@'):
                    command_end = i
                    break

        if command_start is not None and command_end is not None:
            command_code = lines[command_start:command_end]
    
    return ''.join(command_code)

def search_file(directory, search: str):
        for item in directory.iterdir():
            if item.is_dir() and ("vs" not in item.name.lower() and "cache" not in item.name.lower() and "git" not in item.name.lower()):
                result = search_file(item, search) 
                if result:
                    return result
            elif item.is_file() and search.lower() in item.name.lower():
                return item
        return None

async def find_file_and_extract_lines(search_str, start_line, end_line):
    project_root = GetProjectPath() 
    file_path = search_file(Path(project_root), search_str)
    print(file_path)
    if file_path:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            lines = await file.readlines()
            extracted_lines = lines[max(0, start_line - 1):min(end_line, len(lines))]
            return ''.join(extracted_lines)

    return None

