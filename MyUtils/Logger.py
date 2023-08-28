import os
import logging
from datetime import datetime
from contextlib import contextmanager


def get_logger(logger_name, dir_path=None, file_name=''):
    formatter = logging.Formatter("%(asctime)s - %(message)s")

    # setup file handler
    if dir_path is None:
        dir_path = './txt'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_name = file_name.format(datetime.now())
    file_path = os.path.join(dir_path, file_name)
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # setup stream handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers = [file_handler, console_handler]

    return logger


class Logger:
    instance = None

    def __init__(self, logger=None):
        if self.instance is not None:
            self.instance = logger

    def log(self, msg, level=logging.INFO):
        if self.instance is not None:
            self.instance.log(level, msg)
        else:
            print(datetime.now(), ' | ', msg)

    @contextmanager
    def log_duration(self, task_name, level=logging.INFO):
        self.log('Started ' + task_name, level)
        yield None
        self.log('Ended ' + task_name, level)

    def log_error(self, msg, level=logging.INFO):
        self.log('ERROR | ' + msg, level)


def init_logger(logger_name, dir_path=None, file_name=''):
    logger = get_logger(logger_name, dir_path=dir_path, file_name=file_name)
    Logger(logger)


theLogger = Logger()
