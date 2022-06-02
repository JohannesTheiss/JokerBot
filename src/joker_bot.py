import discord
from discord.ext import commands
import time

from src.log.logger import Logger

class JokerBot(commands.Bot):

    # plugins
    PLUGINS = [
        'src.util.help',
        'src.util.util',
        'src.roles.roles',
        'src.error.commandErrorHandler',
        'src.math.math',
        'src.voice.voiceCog'
    ]
    PREFIX = '!'

    def __init__(self):
        super().__init__(command_prefix=self.PREFIX,
                         intents=discord.Intents.all(),
                         help_command=None,
                         case_insensitive=True)

        # create joker_bot logger
        self.logger = Logger(__name__).get()

    # load all plugins to the Bot
    def load_plugins(self, plugins):
        for plug in plugins:
            self.load_extension(plug)

    async def on_ready(self):
        self.logger.info('Logged in as {0.user}'.format(self))

        self.load_plugins(self.PLUGINS)

        # Setting Listening status
        # await self.change_presence( \
                                   # activity=discord.Activity(
                                       # type=discord.ActivityType.listening,
                                       # name="187",
                                       # url="https://www.youtube.com/watch?v=CzlOERhLEFw"))

        # Setting Streaming status
        await self.change_presence(
                activity=discord.Streaming(
                    name='Ejakulat101',
                    url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                )

        # Setting Watching status
        # await self.change_presence( \
                                   # activity=discord.Activity(
                                       # type=discord.ActivityType.watching,
                                       # name='Porn',
                                       # url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))

