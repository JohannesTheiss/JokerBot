import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# append the JokerBot dir to the PATH env. var.
file_path = str(Path(__file__).parent)
sys.path.append(file_path)

from src.joker_bot import JokerBot

def main():
    # load .env
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    joker_bot = JokerBot()
    joker_bot.run(TOKEN)

if __name__ == '__main__':
    main()
