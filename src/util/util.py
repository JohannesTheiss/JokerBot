import discord
from discord.ext import commands

import qrcode
import subprocess
from gtts import gTTS
import random

from io import BytesIO, TextIOWrapper

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

    # def is_connected(self, ctx):
        # voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        # return voice_client and voice_client.is_connected()

    async def connect_to_voice_channel(self, ctx):
        user = ctx.author

        # if user is connect to a voice channel
        # TODO catch if command on DM
        if user.voice and (user.voice.channel != None):
            voice_channel = user.voice.channel
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

            # if the bot is not connected to the voice channel of the user
            if not (voice_client and voice_client.is_connected()):
                voice_client = await voice_channel.connect()

            return voice_client

        else:
            # TODO throw error
            # if user is not connect to a voice channel
            self.logger.warning(f'say : User {user} is not connect to a voice channel')
            await user.send('Du musst in einem Voice-Channel sein')
            return None

    def play_audio_file(self, voice_client, pathToAudioFile):
        if (voice_client != None) and voice_client.is_connected():
            voice_client.loop = False
            voice_client.play(discord.FFmpegPCMAudio(pathToAudioFile))

    def text_to_mp3(self, text, outputFilename):
        tts = gTTS(text=text,
                     lang='de',
                     tld='ch',
                     slow=False)
        tts.save(outputFilename)

    async def read_text(self, ctx, text):
        voice_client = await self.connect_to_voice_channel(ctx)
        if voice_client != None: # TODO if there is a error then we dont need this if
            audio_filename = 'tts.mp3'
            self.text_to_mp3(text, audio_filename)
            self.play_audio_file(voice_client, audio_filename)

    def find_channel_by_name(self, ctx, channel_name):
        for channel in ctx.guild.text_channels:
            if channel.name == channel_name:
                return channel
        return None


    @commands.command()
    async def leave(self, ctx):
        text = 'Tschüsseldorf'
        await ctx.voice_client.disconnect()

    @commands.command()
    async def daniel(self, ctx):
        user = ctx.author
        self.logger.info(f'daniel : {user}')
        voice_client = await self.connect_to_voice_channel(ctx)

        if voice_client != None: # TODO if there is a error then we dont need this if
            self.play_audio_file(voice_client, 'Daniel.flac')


    @commands.command()
    async def say(self, ctx, *, text):
        user = ctx.author
        self.logger.info(f'say : {user} -> {text}')
        await self.read_text(ctx, text)

    @commands.command()
    async def read(self, ctx, channel_name):
        user = ctx.author
        self.logger.info(f'read : {user} -> {channel_name}')

        # find channel by name
        channel = self.find_channel_by_name(ctx, channel_name)
        if channel == None:
            # TODO add execption
            return

        messages = await channel.history(limit=1000).flatten()
        pos = random.randint(0, len(messages)-1)
        text = messages[pos].content

        #await ctx.invoke(self.bot.get_command('say'), text=text)
        await self.read_text(ctx, text)

        await ctx.send(f'> {text}')



# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(Util(bot))
