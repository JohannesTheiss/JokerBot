import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# append the JokerBot dir to the PATH env. var.
sys.path.append(str(Path(__file__).parent))

from src.joker_bot import JokerBot
from src.log.logger import Logger

def createDir(path):
    try:
        if not os.path.isdir(path):
            os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    return path

def setup():
    # create the needed directories
    pathToProject = os.path.dirname(os.path.realpath(__file__))
    createDir(pathToProject + '/logs')
    createDir(pathToProject + '/json')

def main():
    # set the project up
    setup()

    # load .env
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # create main logger
    logger = Logger(__name__).get()
    logger.info('Starting JokerBot...')

    # start the JokerBot
    joker_bot = JokerBot()
    joker_bot.run(TOKEN)

    logger.info('Terminate JokerBot...')

if __name__ == '__main__':
    main()
