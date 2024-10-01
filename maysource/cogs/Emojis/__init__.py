from disnake.ext import commands
import os
import importlib

class EmojiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.desc = "COG for emoji commands"
        self.folder = "dir_name"
        self.load_commands()

    def load_commands(self):
        directory = os.path.dirname(__file__)
        package_name = __name__

        for filename in os.listdir(directory):
            if filename.endswith('.py') and filename.startswith('COMMAND_'):
                module_name = filename[:-3]
                module = importlib.import_module(f".{module_name}", package=package_name)
                if hasattr(module, 'setup_command'):
                    command = module.setup_command(self)
                    cmd = self.bot.get_command(command.name)
                    cmd.extras["group"] = self.__class__.__name__

def setup(bot):
    bot.add_cog(EmojiCog(bot))
