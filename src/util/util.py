import discord
from discord.ext import commands

import qrcode
import subprocess

from src.log.logger import Logger

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # create util logger
        self.logger = Logger(__name__).get()

    @commands.command()
    async def qrcode(self, ctx, text):
        img = qrcode.make(text)
        savedImg = img.save("geeks.jpg")
        self.logger.info("{}: qrcode: {}".format(str(ctx.author), text))
        await ctx.send(file=discord.File('geeks.jpg'))

    @commands.command()
    async def hex(self, ctx, text):
        text = text.encode('utf-8')
        text_hex = text.hex()
        self.logger.info("{}: hex: {} -> {}".format(str(ctx.author), text, text_hex))
        await ctx.send(text_hex)

    # use https://pypi.org/project/psutil/
    #@commands.command()
    #async def uptime(self, ctx):
     #   temp = subprocess.check_output(['sh', '-c', 'uptime -p'])
      #  s = ' '.join(str(temp.decode("utf-8")).split())
       # self.logger.info("{}: uptime: {} ".format(str(ctx.author), s))
      #  await ctx.send(s)


# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(Util(bot))
