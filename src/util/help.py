import discord
from discord.ext import commands

from src.log.logger import Logger

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

    # on !help 
    async def send_bot_help(self, mapping):
        self.logger.info(f'help : {self.context.author}')

        embed = discord.Embed(title="Help", color=0x56358e)
        for cog, commands in mapping.items():
           command_signatures = [self.get_command_signature(c) for c in commands]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    # on !help <command>
    async def send_command_help(self, command):
        self.logger.info(f'help {command.name} : {self.context.author}')

        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    # on !help 
    async def send_group_help(self, group):
        """This is triggered when !help <group> is invoked."""
        await self.context.send("This is the help page for a group command")

    async def send_cog_help(self, cog):
        """This is triggered when !help <cog> is invoked."""
        await self.context.send("This is the help page for a cog")

    async def on_help_command_error(self, ctx, error):
        self.logger.info(f'help_command_error: {command.name} : {self.context.author}')

        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
            await ctx.send(embed=embed)
        else:
            raise error

    async def send_error_message(self, error):
        """If there is an error, send a embed containing the error."""
        self.logger.info(f'error_message: {error}')
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

# is mandatory for a plugins 
def setup(bot):
    bot.help_command = Help()


