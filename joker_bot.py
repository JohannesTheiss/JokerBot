import discord
import qrcode
import os
import subprocess
import numpy as np
import json
import random

from log.logger import *
import integrate



# load .env
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # Setting `Listening ` status
    await client.change_presence(\
            activity=discord.Activity(
                                    type=discord.ActivityType.listening,
                                    name="187",
                                    url="https://www.youtube.com/watch?v=CzlOERhLEFw",
                                    details="lol ok"))
    #user = await client.fetch_user("Dan!el#7786")
    #user = await client.fetch_user("7950")
    #await user.send("Hello there!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'mutter' in message.content.lower() or 'fick' in message.content.lower():
        print("{}: hat mutter oder fick gesagt".format(str(message.author)))
        await message.channel.send('https://tenor.com/view/your-mom-humping-gif-14958931')
        return

    gif = 'https://tenor.com/view/was-bruder-was-soll-ich-sagen-gif-18025423'
    if message.content.startswith('$hello'):
        print("{}: {}".format(str(message.author), "Hallo"))
        await message.channel.send('Hello!')

    elif message.content.startswith('$hafti'):
        print("{}: {}".format(str(message.author), gif))
        await message.channel.send(gif)

    elif message.content.startswith('$sagma '):
        text = message.content.split(' ', 1)[1]
        print("{}: {}".format(str(message.author), text))
        await message.channel.send(text, tts=True)

    elif message.content.startswith('$qrcode '):
        text = message.content.split(' ', 1)[1]
        img = qrcode.make(text)
        savedImg = img.save("geeks.jpg")
        print("{}: qrcode: {}".format(str(message.author), text))
        await message.channel.send(file=discord.File('geeks.jpg'))

    elif message.content.startswith('$hexmitdemex '):
        text = message.content.split(' ', 1)[1].encode('utf-8')
        print("{}: hex: {}".format(str(message.author), text))
        await message.channel.send(text.hex())

    elif message.content.startswith('$cputemp'):
        # das geht nur unter LINUX mit dem cputemp script
        #temp = subprocess.check_output(['zsh', '-c', '. pc.sh; cputemp'])
        #s = ' '.join(str(temp.decode("utf-8")).split())
        #res = "Ich bin **{}** heiß! :hot_pepper::fire:".format(s)
        #print("{}: cputemp: {}".format(str(message.author), s))
        #await message.channel.send(res)
        await message.channel.send("NEIN")

    elif message.content.startswith('$help'):
        lgs = """{
    "M": [
            [2, 3,-1, 0, 0],
            [1, 3, 0,-1, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 2, 3]
         ],
    "V": [1, 0, 0, 1, 1]
}"""
        await message.channel.send(lgs)

    elif message.content.startswith('$lgs '):
        try:
            lgs = message.content.split(' ', 1)[1]
            lgs_dict = json.loads(lgs)
            a = np.array(lgs_dict['M'])
            b = np.array(lgs_dict['V'])
            x = np.linalg.solve(a, b)
            #x = np.array([round(v, 5) for v in x])
            x_string = np.array2string(x, separator=', ', formatter={'float_kind':lambda x: "%.2f" % x})


            # log
            print("{}: lgs: {} ---> {}".format(str(message.author), lgs_dict, x_string))

            # print embed
            embedlist = discord.Embed(title='LGS', \
                                      description='***Carl Friedrich Gauß*** ich küsse deine Augen :heart:',
                                      color=0x2ECC71,
                                      url="https://de.wikipedia.org/wiki/Lineares_Gleichungssystem",
                                      icon_url=message.author.avatar_url)
            embedlist.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/9/9b/Carl_Friedrich_Gauss.jpg")
            embedlist.set_footer(text="{}, du kleiner Schlingel. Diese Angaben sind wie immer ohne Gewähr.".format(message.author.display_name))
            embedlist.add_field(name='Vektor', value='x')
            embedlist.add_field(name='Koeffizienten: [x0, x1, ..., x0]', value=x_string)

            await message.channel.send(embed=embedlist)
        except:
            print("{}: lgs: {} ".format(str(message.author), message.content))
            await message.author.send("So läuft das hier nicht... Ich bauch ein LGS :wink:. (https://de.wikipedia.org/wiki/Lineares_Gleichungssystem)")


    elif message.content.startswith('$uptime'):
        temp = subprocess.check_output(['zsh', '-c', 'uptime -p'])
        s = ' '.join(str(temp.decode("utf-8")).split())
        print("{}: uptime: {} ".format(str(message.author), s))
        await message.channel.send(s)

    elif message.content.startswith('$integrate '):
        #try:
            expression = message.content.split(' ', 1)[1]
            print(expression)

            ex = integrate.integrateExp(expression)
            if ex == -1:
                print("ERROR by ", message.author)
                raise ValueError('A very specific bad thing happened.')

            # log
            print("{}: integrate: {} ---> {}".format(str(message.author), expression, ex))

            img = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.vFEwepavp54qQBpnsDR3nwHaFy%26pid%3DApi&f=1"

            # print embed
            embedlist = discord.Embed(title='Integration', colour=discord.Colour(0x3e038c),
                                      description="∫ {}".format(expression))
            embedlist.set_thumbnail(url=img)
            embedlist.set_footer(text="Powered by Power")

            for s in ex:
                embedlist.add_field(name=s[0], value=s[1].replace("**", "^"), inline=False)

            await message.channel.send(embed=embedlist)

        #except:
            #print("ERROR: {}: {} ".format(str(message.author), message.content))
            #await message.author.send("So läuft das hier nicht...")

    elif 'jokerbot' in message.content.lower():
        print("{}: hat jokerbot gesagt".format(str(message.author)))
        await message.channel.send('Ja ja... du mich auch! :sunglasses:')

    elif "damn boi" == message.content.lower():
        r = round(random.uniform(0, 2))
        print("random i guess ", r)
        l = "YOU"
        if r == 0:
            l = "SHE"
        elif r == 1:
            l = "HE"

        await message.channel.send('{} THICC'.format(l))





client.run(TOKEN)

