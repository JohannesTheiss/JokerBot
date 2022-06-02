import discord
from discord.ext import commands

from src.log.logger import Logger

# class HelpCog(commands.Cog):
    # def __init__(self, bot):
        # self.bot = bot
        # self.prefix = bot.command_prefix

        ## create help logger
        # self.logger = Logger(__name__).get()

    # @commands.command()
    # async def help(self, ctx):
        # self.logger.info(f'{str(ctx.author)}: !help')
        # embed = discord.Embed(title="Help commands", description="Shows various help commands")
        # embed.add_field(name="Show this help", value = f"`{self.prefix}help`", inline = False)
        # embed.add_field(name="Help with a Plugin",
                        # value=f"`{self.prefix}help <plugins>`\ne.g. `{self.prefix}help roles`",
                        # inline=False)
        # embed.add_field(name="Installed Plugins",
                        # value=f":point_right: util\n:point_right: roles",
                        # inline=False)
        # await ctx.send(embed=embed)

class Help(commands.HelpCommand):
    def __init__(self):
        attributes = {
           'name': "help",
           'aliases': ["h", "helps"]
           #'cooldown': commands.Cooldown(2, 5.0, commands.BucketType.user)
        }
        self.command_attrs = attributes

        self.logger = Logger(__name__).get()

    def get_command_signature(self, command):
        return f'{self.clean_prefix}{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping):
        #filtered = await self.filter_commands(self.context.bot.commands, sort=True) # returns a list of command objects
        #names = [command.name for command in filtered] # iterating through the commands objects getting names
        #available_commands = "\n".join(names) # joining the list of names by a new line
        #embed  = discord.Embed(description=available_commands, color=0x56358e)
        #await self.context.send(embed=
        #self.logger.info(f'help : {self.context.author}')

        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           command_signatures = [self.get_command_signature(c) for c in commands]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        """This is triggered when !help <command> is invoked."""
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_group_help(self, group):
        """This is triggered when !help <group> is invoked."""
        await self.context.send("This is the help page for a group command")

    async def send_cog_help(self, cog):
        """This is triggered when !help <cog> is invoked."""
        await self.context.send("This is the help page for a cog")

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
            await ctx.send(embed=embed)
        else:
            raise error

    async def send_error_message(self, error):
        """If there is an error, send a embed containing the error."""
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

# is mandatory for a plugins 
def setup(bot):
    bot.help_command = Help()


