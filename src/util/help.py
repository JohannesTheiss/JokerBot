import discord
from discord.ext import commands

from src.log.logger import Logger

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = bot.command_prefix

        # create help logger
        self.logger = Logger(__name__).get()

    @commands.command()
    async def help(self, ctx):
        self.logger.info(f'{str(ctx.author)}: !help')
        embed = discord.Embed(title="Help commands", description="Shows various help commands")
        embed.add_field(name="Show this help", value = f"`{self.prefix}help`", inline = False)
        embed.add_field(name="Help with a Plugin",
                        value=f"`{self.prefix}help <plugins>`\ne.g. `{self.prefix}help roles`",
                        inline=False)
        embed.add_field(name="Installed Plugins",
                        value=f":point_right: util\n:point_right: roles",
                        inline=False)
        await ctx.send(embed=embed)


# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(HelpCog(bot))
