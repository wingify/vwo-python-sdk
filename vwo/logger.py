import logging
from .helpers import singleton
from logging import WARNING, DEBUG, ERROR, INFO  # noqa:F401
from .helpers import validate_util

_DEFAULT_LOG_FORMAT = 'VWO-SDK - [%(levelname)s]: %(asctime)s %(message)s'
_MIN_LEVEL = logging.ERROR


def update_logger(name, level=None, handler=None):
    if level is None:
        level = _MIN_LEVEL
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = handler or logging.StreamHandler()
    format = logging.Formatter(_DEFAULT_LOG_FORMAT)
    handler.setFormatter(format)

    logger.handlers = [handler]
    return logger


class DefaultLogger():
    """ Class providing log method which logs to stdout. """

    def __init__(self, min_level=_MIN_LEVEL):
        self.logger = update_logger(__name__, level=min_level)
        print('custom logger implemented with level', min_level)


class Logger(singleton.Singleton):

    def __init__(self, logger=None):
        if not logger:
            logger = update_logger(__name__)
        elif isinstance(logger, DefaultLogger):
            logger = logger.logger
        elif validate_util.is_valid_utility(logger, 'logger'):
            logger = logger
        else:
            print('Logger passed doesn"t contaings log functionality, using default logger')  # noqa:E501
            logger = update_logger(__name__)

        self.logger = logger

        # if isinstance(logger, logging.Logger):
        #     print('Singleton Logger initialized with level', logger.level)
        # else:
        #     print('Singleton Logger initialized with custom logger')

    def log(self, level, message):
        try:
            self.logger.log(level, message)
        except Exception:
            self.logger = update_logger(__name__, level=logging.DEBUG)
            self.logger.log(WARNING, 'Logger provided to SDK is broken, initiazlizing SDK with default logger')  # noqa:E501
            self.logger.log(level, message)
