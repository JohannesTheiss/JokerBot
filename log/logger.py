import os
import logging

# CONFIG
LOG_FILE   = "jokerbot"
LOG_DIR    = "logs"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def createDir(name):
    path = os.path.dirname(os.path.realpath(__file__)) + '/' + name
    try:
        if not os.path.isdir(path):
            os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    return path


# Create a custom logger
logger = logging.getLogger(LOG_FILE)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(createDir(LOG_DIR) + '/{}.log'.format(LOG_FILE))
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter(LOG_FORMAT)
f_format = logging.Formatter(LOG_FORMAT)
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

#logger.debug('This is a warning')
#logger.error('This is an error')

