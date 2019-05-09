import logging
from logging import getLogger, StreamHandler, Formatter


class LogSupport(object):
    def __init__(self, loggerName = "DefaultLogger"):
        logger = getLogger(loggerName)
        logger.setLevel(logging.DEBUG)
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(handler_format)
        logger.addHandler(stream_handler)
        self.logger = logger

    def logger(self):
        return self.logger
