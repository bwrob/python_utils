import os
from logging import *
from datetime import datetime
from contextlib import contextmanager
from MyUtils.Singleton import Singleton


class MyLogger(Logger, metaclass=Singleton):
    """
    Wraps standard logging library logger into singleton.
    """

    def __init__(self, logger_name='', dir_path=None, file_name='log_{}.log'):

        super().__init__(logger_name)
        formatter = Formatter("%(asctime)s - %(message)s")

        # setup file handler
        if dir_path is None:
            dir_path = './'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_name = file_name.format(datetime.now().date())
        file_path = os.path.join(dir_path, file_name)
        file_handler = FileHandler(file_path)
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(formatter)

        # setup stream handler
        console_handler = StreamHandler()
        console_handler.setLevel(INFO)
        console_handler.setFormatter(formatter)

        self.setLevel(DEBUG)
        self.handlers = [file_handler, console_handler]

    @contextmanager
    def log_duration(self, task_name, level=INFO):
        self.log(msg='DURATION | Started ' + task_name, level=level)
        yield None
        self.log(msg='DURATION | Ended ' + task_name, level=level)

    def log_error(self, error_msg):
        self.exception(msg='ERROR | ' + error_msg)

    def log_info(self, msg):
        self.log(msg=msg, level=INFO)

    def log_debug(self, msg):
        self.log(msg=msg, level=DEBUG)


theLogger = MyLogger('log')
theLogger.log_debug('Logger initialized.')
