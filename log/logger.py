import os
import logging

# Create a custom logger
logger = logging.getLogger("jokerbot")

# Create handlers
c_handler = logging.StreamHandler()

path = os.path.dirname(os.path.realpath(__file__)) + '/logs'
try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)

f_handler = logging.FileHandler(path + '/jokerbot.log')

c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

#logger.debug('This is a warning')
#logger.error('This is an error')

