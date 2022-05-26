import discord
import sys
import traceback
from discord.ext import commands

from src.log.logger import Logger

class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # create commandErrorHandler logger
        self.logger = Logger(__name__).get()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #The event triggered when an error is raised while invoking a command.
        if isinstance(error, discord.ext.commands.CommandNotFound):
            self.logger.warning(f'CommandError: {str(ctx.author)} -> {str(ctx.command)}')
            await ctx.send('WTF... Was willst du denn von mir???\n*LUL*')
        else:
            self.logger.error('Ignoring exception in command {}:'.format(ctx.command))
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(CommandErrorHandler(bot))
