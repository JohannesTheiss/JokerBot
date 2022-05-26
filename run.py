import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# append the JokerBot dir to the PATH env. var.
#file_path = str(Path(__file__).parent)
sys.path.append(str(Path(__file__).parent))

from src.joker_bot import JokerBot
from src.log.logger import Logger

def main():
    # load .env
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # create main logger
    logger = Logger(__name__).get()
    logger.info('Starting JokerBot...')

    joker_bot = JokerBot()
    joker_bot.run(TOKEN)

    logger.info('Terminate JokerBot...')

if __name__ == '__main__':
    main()
