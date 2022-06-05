import discord
from discord.ext import commands

import json

import numpy as np

from src.math.integration import Integration
from src.log.logger import Logger

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.integration = Integration()

        # create util logger
        self.logger = Logger(__name__).get()

    @commands.command(aliases=['solveLgs'],
                      help="""Solve a given LGS.\ne.g.\n```!lgs {
    "M": [
            [2, 3,-1, 0, 0],
            [1, 3, 0,-1, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 2, 3]
         ],
    "V": [1, 0, 0, 1, 1]
}```""")
    async def lgs(self, ctx, *, lgs):
        try:
            lgs_dict = json.loads(lgs)
            a = np.array(lgs_dict['M'])
            b = np.array(lgs_dict['V'])
            x = np.linalg.solve(a, b)
            #x = np.array([round(v, 5) for v in x])
            x_string = np.array2string(x, separator=', ', formatter={'float_kind':lambda x: "%.2f" % x})

            self.logger.info("{}: lgs: {} -> {}".format(str(ctx.author), lgs_dict, x_string))

            embedlist = discord.Embed(title='LGS', \
                                      description='***Carl Friedrich Gauß*** ich küsse deine Augen :heart:',
                                      color=0x2ECC71,
                                      url="https://de.wikipedia.org/wiki/Lineares_Gleichungssystem",
                                      icon_url=ctx.author.avatar_url)
            embedlist.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/9/9b/Carl_Friedrich_Gauss.jpg")
            embedlist.set_footer(text="{}, du kleiner Schlingel...\nDiese Angaben sind wie immer ohne Gewähr.".format(ctx.author.display_name))
            embedlist.add_field(name='Vektor', value='x')
            embedlist.add_field(name='Koeffizienten: [x0, x1, ..., x0]', value=x_string)

            await ctx.send(embed=embedlist)
        except:
            self.logger.warning("{}: lgs: {} ".format(str(ctx.author), ctx.content))
            await ctx.author.send("So läuft das hier nicht... Ich bauch ein LGS :wink:. (https://de.wikipedia.org/wiki/Lineares_Gleichungssystem)")

    @commands.command(aliases=['integ'],
                      help='Integrate a given expression.\ne.g.\n`!integrate (3/2)-x`')
    async def integrate(self, ctx, *, expression):
        ex = self.integration.integrateExp(expression)
        if ex == -1:
            self.logger.warning(f'integration ERROR by {ctx.author}')
            return

        # log
        self.logger.info("{}: integrate: {} -> {}".format(str(ctx.author), expression, ex))

        embedlist = discord.Embed(title='Integration', colour=discord.Colour(0x3e038c),
                                  description="∫ {}".format(expression))
        embedlist.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.vFEwepavp54qQBpnsDR3nwHaFy%26pid%3DApi&f=1")
        embedlist.set_footer(text="Powered by Power")

        for s in ex:
            embedlist.add_field(name=s[0], value=s[1].replace("**", "^"), inline=False)

        await ctx.send(embed=embedlist)


# is mandatory for a plugins 
def setup(bot):
	bot.add_cog(Math(bot))
