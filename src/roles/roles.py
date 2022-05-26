import discord
from discord.ext import commands

from src.log.logger import Logger

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # create roles logger
        self.logger = Logger(__name__).get()

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
        # channel = member.guild.system_channel
        # if channel is not None:
            # await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def roles(self, ctx):
        print(", ".join([str(r.name) for r in ctx.guild.roles]))


# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(Roles(bot))
