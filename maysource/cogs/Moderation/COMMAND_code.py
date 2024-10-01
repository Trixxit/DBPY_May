import disnake
from disnake.ext import commands
from Utilities.staffchecks import Anystaffcheck
import os

maybot = None

@commands.slash_command(name="code", description="Perform code actions with optional file upload.", guild_ids=[971700371112198194])
@Anystaffcheck((1231831222930636800, 1180945644567941272))
async def codee(
    inter: disnake.ApplicationCommandInteraction,
    action: str,
    filepath: str = None,
    code: str = None,
    file: disnake.Attachment = None
):
    def save_data(filen, data):
        with open(filen, "w") as write_file:
            write_file.write(data)
        with open(filen, "r") as read_file:
            datak = read_file.read()
        return datak

    def load_data(filen):
        try:
            with open(filen, "r") as read_file:
                datad = read_file.read()
        except FileNotFoundError:
            return False
        return datad

    def list_directory(dir_path):
        try:
            items = os.listdir(dir_path)
        except FileNotFoundError:
            return False
        except NotADirectoryError:
            return None
        return items

    def get_file_extension(filepath):
        _, extension = os.path.splitext(filepath)
        return extension

    def is_in_working_directory(filepath):
        cwd = os.getcwd()
        return os.path.commonpath([cwd, filepath]) == cwd

    if action is None:
        await inter.response.send_message("Action not specified.", ephemeral=True)
        return

    if action.startswith("check"):
        if filepath == "None":
            filepath = os.getcwd()
        dir_contents = list_directory(filepath)
        if dir_contents is False:
            await inter.response.send_message(f"No directory found at `{filepath}`", ephemeral=True)
            return
        elif dir_contents is None:
            await inter.response.send_message(f"`{filepath}` is not a directory.", ephemeral=True)
            return

        output = f"Contents of `{filepath}`:\n" + "\n".join(dir_contents)
        if len(output) > 2000:
            with open("directory_contents.txt", "w") as f:
                f.write(output)
            await inter.response.send_message(
                f"Contents of `{filepath}`:",
                file=disnake.File("directory_contents.txt"),
                ephemeral=True
            )
            os.remove("directory_contents.txt")
        else:
            await inter.response.send_message(
                f"Contents of `{filepath}`:\n```\n" + "\n".join(dir_contents) + "\n```",
                ephemeral=True
            )

    elif action.startswith("read"):
        if filepath is None:
            await inter.response.send_message("Filepath not stated.", ephemeral=True)
            return
        
        absolute_path = os.path.abspath(filepath)
        file_content = load_data(absolute_path)
        
        if file_content is False:
            await inter.response.send_message(
                f"No file found at `{filepath}` (absolute path: `{absolute_path}`)",
                ephemeral=True
            )
            return
        
        if len(file_content) > 2000:
            output_filename = "reading_" + str(os.path.basename(filepath))
            with open(output_filename, "w") as f:
                f.write(file_content)
            
            # Send the file and a message in one response
            try:
                await inter.response.send_message(
                    content=f"Content of `{filepath}` (file attached):",
                    file=disnake.File(output_filename),
                    ephemeral=True
                )
            finally:
                # Ensure the file is removed after sending
                if os.path.exists(output_filename):
                    os.remove(output_filename)
        
        else:
            # Send the content directly if it fits within the limit
            await inter.response.send_message(
                content=f"Content of `{filepath}`:\n```\n{file_content}\n```",
                ephemeral=True
            )

    elif action.startswith("write"):
        if filepath is None:
            await inter.response.send_message("Filepath not stated.", ephemeral=True)
            return

        if file is not None:
            # Save uploaded file
            absolute_path = os.path.abspath(filepath)
            await file.save(absolute_path)
            await inter.response.send_message(f"Saved uploaded file to `{filepath}`", ephemeral=True)
        
        elif code:
            # Save text content
            code_content = code
            absolute_path = os.path.abspath(filepath)
            saved_content = save_data(absolute_path, code_content)
            await inter.response.send_message(
                f"Saved code to `{filepath}`:\n```\n{saved_content}\n```",
                ephemeral=True
            )
        
        else:
            await inter.response.send_message("No code or file provided.", ephemeral=True)

    elif action.startswith("delete"):
        if filepath is None:
            await inter.response.send_message("Filepath not stated.", ephemeral=True)
            return
        
        absolute_path = os.path.abspath(filepath)
        os.remove(absolute_path)
        await inter.response.send_message(
            f"Deleting `{filepath}` (absolute path: `{absolute_path}`)",
            ephemeral=True
        )

    else:
        await inter.response.send_message(
            "No valid command given. Use `check`, `read`, `delete`, or `write`",
            ephemeral=True
        )

@commands.command(name="code", description="Code actions")
@Anystaffcheck((1231831222930636800, 1180945644567941272))
async def code(ctx, filepath: str = None, *, code: str = None):
    def save_data(filen, data):
        with open(filen, "w") as write_file:
            write_file.write(data)
        with open(filen, "r") as read_file:
            datak = read_file.read()
        return datak

    def load_data(filen):
        try:
            with open(filen, "r") as read_file:
                datad = read_file.read()
        except FileNotFoundError:
            return False
        return datad

    def list_directory(dir_path):
        try:
            items = os.listdir(dir_path)
        except FileNotFoundError:
            return False
        except NotADirectoryError:
            return None
        return items

    def get_file_extension(filepath):
        _, extension = os.path.splitext(filepath)
        return extension

    def is_in_working_directory(filepath):
        cwd = os.getcwd()
        return os.path.commonpath([cwd, filepath]) == cwd

    if code is None:
        await ctx.send("Code action not stated.")
        return

    if code.startswith("check"):
        if filepath == "None":
            filepath = os.getcwd()
        dir_contents = list_directory(filepath)
        if dir_contents is False:
            await ctx.send(f"No directory found at `{filepath}`")
            return
        elif dir_contents is None:
            await ctx.send(f"`{filepath}` is not a directory.")
            return

        output = f"Contents of `{filepath}`:\n" + "\n".join(dir_contents)
        if len(output) > 2000:
            with open("directory_contents.txt", "w") as f:
                f.write(output)
            await ctx.send(f"Contents of `{filepath}`:", file=disnake.File("directory_contents.txt"))
            os.remove("directory_contents.txt")
        else:
            await ctx.send(f"Contents of `{filepath}`:\n```\n" + "\n".join(dir_contents) + "\n```")

    elif code.startswith("read"):
        if filepath is None:
            await ctx.send("Filepath not stated.")
            return
        
        absolute_path = os.path.abspath(filepath)
        await ctx.send(f"Attempting to read from `{absolute_path}`")
        file_content = load_data(absolute_path)
        if file_content is False:
            await ctx.send(f"No file found at `{filepath}` (absolute path: `{absolute_path}`)")
            return

        if len(file_content) > 2000:
            output_filename = "reading_" + str(os.path.basename(filepath))
            with open(output_filename, "w") as f:
                f.write(file_content)
            await ctx.send(f"Content of `{filepath}`:", file=disnake.File(output_filename))
            os.remove(output_filename)
        else:
            await ctx.send(f"Content of `{filepath}`:\n```\n{file_content}\n```")

    elif code.startswith("write"):
        if filepath is None:
            await ctx.send("Filepath not stated.")
            return

        if not code[6:]:
            if len(ctx.message.attachments) > 0:
                attachment = ctx.message.attachments[0]
                await attachment.save(filepath)
                await ctx.send(f"Saved attachment to `{filepath}`")
            else:
                await ctx.send("No code provided and no attachment found.")
        
        else:
            code_content = code[6:]
            absolute_path = os.path.abspath(filepath)
            await ctx.send(f"Attempting to write to `{absolute_path}`")
            saved_content = save_data(absolute_path, code_content)
            await ctx.send(f"Saved code to `{filepath}`:\n```\n{saved_content}\n```")

    elif code.startswith("delete"):
        if filepath is None:
            await ctx.send("Filepath not stated.")
            return
        
        absolute_path = os.path.abspath(filepath)
        os.remove(absolute_path)
        await ctx.send(f"Deleting `{filepath}` (absolute path: `{absolute_path}`)")
    
    else:
        await ctx.send("No valid command given. Use `check`, `read`, `delete`, or `write`")

def setup_command(cog):
    global maybot
    maybot = cog.bot
    cog.bot.add_command(code)
    cog.bot.add_slash_command(codee)
    return code
