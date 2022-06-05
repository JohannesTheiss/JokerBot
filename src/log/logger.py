import os
import sys
import logging


class Logger:

    LOG_FORMAT = logging.Formatter('[%(asctime)s] - %(name)-25s - %(levelname)-8s - %(message)s')

    def __init__(self, logger_name):
        self.logger_name = logger_name

        # if logger already exists then just get it and return
        if self.logger_name in logging.root.manager.loggerDict:
            self.logger = logging.getLogger(self.logger_name)
            return

        # create or get a custom logger
        self.logger = logging.getLogger(self.logger_name)

        # set default logging level
        self.logger.setLevel(logging.DEBUG)

        # create the logs directory
        self.pathToLogs = os.path.dirname(os.path.realpath(__file__)) + '/../../logs'

        # add the handler
        self.addConsoleHandler()
        self.addFileHandler(self.logger_name)
        self.addFileHandler('all_logs')

    def get(self):
        return self.logger

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

