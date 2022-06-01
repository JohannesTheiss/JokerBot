import discord
from discord.ext import commands

import qrcode
import subprocess
from gtts import gTTS
import random

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


    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def daniel(self, ctx):
        user = ctx.author
        voice_channel = user.voice.channel

        if voice_channel != None:
            voice_client = await self.connect_to_channel(ctx, voice_channel)
            voice_client.loop = False
            voice_client.play(discord.FFmpegPCMAudio('Daniel.flac'))

    def is_connected(self, ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    async def connect_to_channel(self, ctx, voice_channel):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if not (voice_client and voice_client.is_connected()):
            voice_client = await voice_channel.connect()
        return voice_client

    @commands.command()
    async def say(self, ctx, *, text):
        user = ctx.author
        voice_channel = user.voice.channel

        if voice_channel != None:

            myobj = gTTS(text=text, lang='de', tld='ch', slow=False)
            myobj.save("welcome.mp3")

            voice_client = await self.connect_to_channel(ctx, voice_channel)
            voice_client.loop = False
            voice_client.play(discord.FFmpegPCMAudio('welcome.mp3'))

    async def sag(self, ctx, text):
        user = ctx.author
        voice_channel = user.voice.channel
        if voice_channel != None:
            myobj = gTTS(text=text, lang='de', tld='ch', slow=False)
            myobj.save("welcome.mp3")

            voice_client = await self.connect_to_channel(ctx, voice_channel)
            voice_client.loop = False
            voice_client.play(discord.FFmpegPCMAudio('welcome.mp3'))

    @commands.command()
    async def leave(self, ctx):
        text = 'Tschüsseldorf'
        await ctx.voice_client.disconnect()

    @commands.command()
    async def read(self, ctx, channel_name):
        channels = ctx.guild.text_channels

        channel = None
        for c in channels:
            if c.name == channel_name:
                channel = c


        messages = await channel.history(limit=1000).flatten()

        #for msg in messages:
            #print(msg.content)

        pos = random.randint(0, len(messages))
        print(len(messages))

        text = messages[pos].content

        user = ctx.author
        voice_channel = user.voice.channel
        if voice_channel != None:
            myobj = gTTS(text=text, lang='de', tld='ch', slow=False)
            myobj.save("welcome.mp3")

            voice_client = await self.connect_to_channel(ctx, voice_channel)
            voice_client.loop = False
            voice_client.play(discord.FFmpegPCMAudio('welcome.mp3'))

        await ctx.send(f'> {text}')



# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(Util(bot))
