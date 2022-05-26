import os
import sys
import logging


class Logger:
    LOG_DIR    = "logs"
    LOG_FORMAT = logging.Formatter('[%(asctime)s] - %(name)-25s - %(levelname)-8s - %(message)s')

    def __init__(self, logger_name):
        self.logger_name = logger_name

        # create a custom logger
        self.logger = logging.getLogger(self.logger_name)

        # set default logging level
        self.logger.setLevel(logging.DEBUG)

        # create the logs directory
        self.pathToLogs = self.createDir()

        # add the handler
        self.addConsoleHandler()
        self.addFileHandler(self.logger_name)
        self.addFileHandler('all_logs')

    def get(self):
        return self.logger

    def createDir(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/../../' + self.LOG_DIR
        try:
            if not os.path.isdir(path):
                os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        return path

    def addConsoleHandler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(self.LOG_FORMAT)

        # add console handler to the logger
        self.logger.addHandler(console_handler)


    def addFileHandler(self, log_file_name):
        file_handler = logging.FileHandler(f'{self.pathToLogs}/{log_file_name}.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(self.LOG_FORMAT)

        # add file handler to the logger
        self.logger.addHandler(file_handler)

