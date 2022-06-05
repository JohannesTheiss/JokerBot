import discord
from discord.ext import commands

import qrcode
import subprocess

from datetime import datetime

from src.log.logger import Logger

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # create util logger
        self.logger = Logger(__name__).get()

        # start uptime timer
        self.start_time = datetime.now()

    def format_time_delta(self, time_delta, fmt):
        d = {"days": time_delta.days}
        d["hours"], rem = divmod(time_delta.seconds, 3600)
        d["minutes"], d["seconds"] = divmod(rem, 60)
        return fmt.format(**d)

    @commands.command(aliases=['qrc', 'qr'],
                      help='Create a QR-Code from the input text.\ne.g.\n`!qrcode Hello World`')
    async def qrcode(self, ctx, *, text):
        img = qrcode.make(text)
        savedImg = img.save("geeks.jpg")
        self.logger.info("{}: qrcode: {}".format(str(ctx.author), text))
        await ctx.send(file=discord.File('geeks.jpg'))

    @commands.command(aliases=['textToHex'],
                      help='Convert the input text to Hex.\ne.g.\n`!hex Hello World`')
    async def hex(self, ctx, *, text):
        text = text.encode('utf-8')
        text_hex = text.hex()
        self.logger.info("{}: hex: {} -> {}".format(str(ctx.author), text, text_hex))
        await ctx.send(text_hex)

    @commands.command(aliases=['upt'],
                      help='Get the uptime of the bot.\ne.g.\n`!uptime`')
    async def uptime(self, ctx):
        time_delta = datetime.now() - self.start_time
        time_delta_format = '```Days:     {days}\nHours:    {hours}\nMinutes:  {minutes}\nSeconds:  {seconds}```'
        uptime_str = self.format_time_delta(time_delta, time_delta_format)

        self.logger.info(f'uptime : {ctx.author} -> {repr(uptime_str)}')
        await ctx.send(uptime_str)

# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(Util(bot))
