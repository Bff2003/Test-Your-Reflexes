import logging
import os
from datetime import datetime

class Logger:

    LOGGERS_LIST = []

    def __init__(self, name, log_file='app.log', level=logging.INFO, specific_log_file=False):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create a file handler
        if not os.path.exists('logs'):
            os.makedirs('logs')
        log_file_path = os.path.join('logs', log_file)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(level)

        if specific_log_file:
            log_file_path = os.path.join('logs', f'{name}.log')
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(level)
            self.logger.addHandler(file_handler)


        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create a formatter and set it for both handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger