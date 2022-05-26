import discord
from discord.ext import commands
import json
import os

from src.log.logger import Logger
from src.data.models.roleLink import RoleLink

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # create roles logger
        self.logger = Logger(__name__).get()
        self.roleLinks = {}
        self.pathToJson = os.path.dirname(os.path.realpath(__file__)) + '/../../json/roleLinks.json'

        self.loadRoleLinksFromJson()

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
        # channel = member.guild.system_channel
        # if channel is not None:
            # await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def allRoles(self, ctx):
        self.logger.info(f'{ctx.guild.name}::{str(ctx.author)} get all roles')
        roles = ctx.guild.roles

        embed = discord.Embed(title="Available roles", color=0x019ba0)
        embed.add_field(name="Roles", value=' '.join([str(role.mention) for role in roles]), inline=True)

        await ctx.send(embed=embed)

    # @commands.command()
    # async def myRoles(self, ctx):
        # roles = ctx.author.roles

        # embed = discord.Embed(title=f"Your roles",
                              # description=f'{str(ctx.author.mention)}',
                              # color=ctx.author.color)
        # embed.add_field(name="->", value=' '.join([str(role.mention) for role in roles]), inline=True)

        # await ctx.send(embed=embed)

    @commands.command()
    async def addRoleLink(self, ctx, role : discord.Role, link : str):
        self.logger.info(f'{ctx.guild.name}::{str(ctx.author)} add new role link: "{role.name}" <-> "{link}"')

        roleLink = RoleLink(role, link)

        guild_id = ctx.guild.id
        if guild_id in self.roleLinks:
            self.roleLinks[guild_id].append(roleLink)
        else:
            self.roleLinks[guild_id] = [roleLink]

        await ctx.send(f'Added Role-Link-Connection for: {role.mention}')

    @commands.command()
    async def getRoleLinks(self, ctx):
        self.logger.info(f'{ctx.guild.name}::{str(ctx.author)} get role links')

        guild_id = ctx.guild.id
        if not (guild_id in self.roleLinks):
            return

        embed = discord.Embed(title=f"All active Role-Links",
                              color=0x4193ff,
                              url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        # embed.set_author(name='JokerBot', url='https://github.com/JohannesTheiss/JokerBot',
                         # icon_url='https://cdn.discordapp.com/avatars/839158597781946379/b248a0175471aca4cbadab0dd9ef2b7c.png?size=256')
        embed.set_thumbnail(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.KEQYFeX1x-PAOnZWAqTxxQHaE8%26pid%3DApi&f=1')
        embed.set_footer(text='Powered by *DEINER MOM*')
        for roleLink in self.roleLinks[guild_id]:
            embed.add_field(name=f'\u200b', value=f'{roleLink.get_role().mention} :arrow_right: {roleLink.get_link()}', inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def saveRoleLinks(self, ctx):
        self.logger.info(f'{ctx.guild.name}::{str(ctx.author)} save role links to json')

        if ctx.author.id == 317769221079695360:
            self.saveRoleLinksToJson()

        await ctx.send("Saved")

    def saveRoleLinksToJson(self):
        role_link_json_dict = {}
        for guild_id in self.roleLinks.keys():
            rl = []
            for role_link in self.roleLinks[guild_id]:
                rl.append(role_link.as_dict())

            role_link_json_dict[guild_id] = rl

        with open(self.pathToJson, 'w') as file:
            json.dump(role_link_json_dict, file)

    def loadRoleLinksFromJson(self):
        if not os.path.exists(self.pathToJson):
            self.logger.warning(f'path to the json file doesn\'t exists "{self.pathToJson}"')
            return

        role_link_json_dict = {}
        # read from json
        with open(self.pathToJson, 'r+') as file:
            role_link_json_dict = json.load(file)

        # map the Json dict to a python dict
        number_of_rolelinks = 0
        for guild_id_str in role_link_json_dict.keys():
            guild_id_int = int(guild_id_str)

            # get guild by id
            guild = self.bot.get_guild(guild_id_int)
            if guild == None:
                self.logger.error(f'Guild not found guild_id: {guild_id_int}')
                continue

            number_of_rolelinks = number_of_rolelinks + len(role_link_json_dict[guild_id_str])
            rl = []
            for role_dict in role_link_json_dict[guild_id_str]:
                role = guild.get_role(role_dict['role_id'])
                rl.append(RoleLink(role, role_dict['link']))

            self.roleLinks[guild_id_int] = rl

        self.logger.info(f'Loaded all role links from json')
        self.logger.info(f'number_of_server: {len(self.roleLinks.keys())} total_number_roleLinks: {number_of_rolelinks}')



# is mandatory for a plugin 
def setup(bot):
	bot.add_cog(Roles(bot))
