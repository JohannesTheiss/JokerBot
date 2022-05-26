import sys

from pathlib import Path

# discord.py imports
import discord
from discord.ext import commands


# append the src dir to the PATH env. var.
#file_path = str(Path(__file__).parent)
#sys.path.append(file_path)

# import local files
#from log import *
#from roles.roles import Roles
#from util.util import Util
#from util.help import HelpCog



# setting up the Bot
#intents = discord.Intents.all()
#PREFIX = '!'
# bot = commands.Bot(command_prefix=PREFIX,
                   # intents=intents,
                   # help_command=None)

class JokerBot(commands.Bot):

    # plugins
    PLUGINS = ['util.help', 'util.util', 'roles.roles']
    PREFIX = '!'

    def __init__(self):


        super().__init__(command_prefix=self.PREFIX,
                         intents=discord.Intents.all(),
                         help_command=None)

        self.load_plugins(self.PLUGINS)


    # load all plugins to the Bot
    def load_plugins(self, plugins):
        for plug in plugins:
            self.load_extension(plug)

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

        # Setting `Listening ` status
        await self.change_presence(\
                activity=discord.Activity(
                                        type=discord.ActivityType.listening,
                                        name="187",
                                        url="https://www.youtube.com/watch?v=CzlOERhLEFw",
                                        details="lol ok"))

        #user = await client.fetch_user("Dan!el#7786")
        #user = await client.fetch_user("7950")
        #await user.send("Hello there!")



#bot.run(TOKEN)

