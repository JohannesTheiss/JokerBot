import discord
from discord.ext import commands

import qrcode
import subprocess

import time
import datetime

from src.log.logger import Logger

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # create util logger
        self.logger = Logger(__name__).get()

        # start uptime timer
        self.start_time = time.time()

    @commands.command()
    async def qrcode(self, ctx, *, text):
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

    @commands.command()
    async def uptime(self, ctx):
        time_delta = datetime.timedelta(seconds=int(round(time.time()-self.start_time)))
        seconds = time_delta.seconds
        uptime_str = f'```Days:     {time_delta.days}\nHours:    {seconds // 3600}\nMinutes:  {seconds // 60}\nSeconds:  {seconds}```'

        self.logger.info(f'uptime : {ctx.author} -> {repr(uptime_str)}')
        await ctx.send(uptime_str)

# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(Util(bot))
