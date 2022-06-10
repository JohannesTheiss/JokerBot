import discord
from discord.ext import commands
from gtts import gTTS
import random

from src.log.logger import Logger

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # create help logger
        self.logger = Logger(__name__).get()

    async def connect_to_voice_channel(self, ctx):
        user = ctx.author
        self.logger.info("connect_to_voice_channel")

        # if user is connect to a voice channel
        # TODO catch if command on DM
        #if user.voice and (user.voice.channel != None):
        if user.voice and user.voice.channel:
            voice_channel = user.voice.channel
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

            vc_str_list = [str(e) for e in ctx.bot.voice_clients]

            self.logger.info("all curr voice clients :" + ', '.join(vc_str_list))
            self.logger.info("user channel : " + str(voice_channel))
            self.logger.info("user guild: " + str(ctx.guild))
            self.logger.info("voice_client: : " + str(voice_client))

            # if the bot is connect with the voice_client
            #if voice_client and voice_client.is_connected():

            # if voice_client exists
            if voice_client:
                self.logger.info("selected client :" + str(voice_client) + " " + str(voice_client.channel) + " " + str(voice_client.guild))
                self.logger.info("voice_client id connected: " + str(voice_client.is_connected()))

                if voice_client.is_connected():

                    if voice_client.channel == voice_channel:
                        self.logger.info("voice_client.channel == voice_channel => True")
                    else:
                        self.logger.info("move to channel: " + str(voice_channel) + " ...")
                        await voice_client.move_to(voice_channel)
                        self.logger.info("moved")
                #else:
                    #pass
                    # reconnect
                    #print("disconnect..")
                    #await voice_client.disconnect()
                    #print("reconnect...")
                    #voice_client = await voice_channel.connect()
#

                # the move to the voice channel
                #await voice_client.move_to(voice_channel)

                #await voice_channel.disconnect()
                #voice_client = await voice_client.connect()
                # update voice_client
                #voice_client = discord.utils.get(ctx.bot.voice_clients + guild=ctx.guild)

                voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
                self.logger.info("post move client :" + str(voice_client) + " " + str(voice_client.channel) + " " + str(voice_client.guild))

            else:
                self.logger.info("connect...")
                # else connect the voice_client to the voice_channel
                voice_client = await voice_channel.connect(timeout=3, reconnect=True)

                self.logger.info("post connect client :" + str(voice_client) + " " + str(voice_client.channel) + " " + str(voice_client.guild))

            # if the bot is not connected to the voice channel of the user
            #if not (voice_client and voice_client.is_connected()):
                #voice_client = await voice_channel.connect()

            self.logger.info("bot channel: " + str(voice_client.channel))

            self.logger.info("connect_to_voice_channel END")
            return voice_client

        else:
            # TODO throw error
            # if user is not connect to a voice channel
            self.logger.warning(f'say : User {user} is not connect to a voice channel')
            await user.send('Du musst in einem Voice-Channel sein')
            return None

    def play_audio_file(self, voice_client, pathToAudioFile):
        if (voice_client != None) and voice_client.is_connected():
            #voice_client.loop = False
            voice_client.play(discord.FFmpegPCMAudio(pathToAudioFile))

    def text_to_mp3(self, text, outputFilename):
        tts = gTTS(text=text,
                     #lang='ja',
                     #lang='es',
                     #lang='it',
                     lang='de',
                     #tld='ch',
                     #tld='co.za',
                     slow=False)
        tts.save(outputFilename)

    async def read_text(self, ctx, text):
        voice_client = await self.connect_to_voice_channel(ctx)
        if voice_client != None: # TODO if there is a error then we dont need this if

            self.logger.info("read_text voice_client: " + str(voice_client.channel))

            audio_filename = 'tts.mp3'
            self.text_to_mp3(text, audio_filename)
            self.play_audio_file(voice_client, audio_filename)

    def find_channel_by_name(self, ctx, channel_name):
        for channel in ctx.guild.text_channels:
            if channel.name == channel_name:
                return channel
        return None


    @commands.command(help='Tell the bot to leave the voice channel.\ne.g.\n`!leave`')
    async def leave(self, ctx):
        text = 'Tschüsseldorf'
        await ctx.voice_client.disconnect()

    @commands.command(aliases=['loser', 'dan'],
                      help='Ruft den LOSER.\ne.g.\n`!daniel`')
    async def daniel(self, ctx):
        user = ctx.author
        self.logger.info(f'daniel : {user}')
        voice_client = await self.connect_to_voice_channel(ctx)

        if voice_client != None: # TODO if there is a error then we dont need this if
            #self.play_audio_file(voice_client, 'Daniel.flac')
            self.play_audio_file(voice_client, 'daniel2.m4a')


    @commands.command(aliases=['s', 'sag', 'saz'],
                      help='The bot reads the input text.\ne.g.\n`!say Hallo lol`')
    async def say(self, ctx, *, text):
        user = ctx.author
        self.logger.info(f'say : {user} -> {text}')
        await self.read_text(ctx, text)

    @commands.command(aliases=['r'],
                      help='The bot reads a random message from the given text channel.\ne.g.\n`!read general`')
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
        msg = messages[pos]
        text = msg.content

        #await ctx.invoke(self.bot.get_command('say'), text=text)
        await self.read_text(ctx, text)

        embed = discord.Embed()
        embed.description = f'[Message]({msg.jump_url})\n```{msg.content}```'
        await ctx.send(embed=embed)

# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(Voice(bot))
