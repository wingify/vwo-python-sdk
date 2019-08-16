from __future__ import print_function
import logging
from logging import INFO, DEBUG, WARNING, ERROR  # noqa: F401
from .helpers import singleton
from .helpers import validate_util
from .helpers.enums import LogLevelEnum, LogMessageEnum, FileNameEnum

_DEFAULT_LOG_FORMAT = 'VWO-SDK - [%(levelname)s]: %(asctime)s %(message)s'
_DEFAULT_LEVEL = logging.ERROR


def update_logger(name, level=_DEFAULT_LEVEL, handler=None):
    """ Resets logging.Logger instance of given name with given level and handler.

    Args:
        name (string): constant name for logger
        level (int): numerical value of level usually between, 0 to 50
        handler (logging.handlers): a handler logger instance

    Returns:
        logging.Logger: A logging.Logger object
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = handler or logging.StreamHandler()
    format = logging.Formatter(_DEFAULT_LOG_FORMAT)
    handler.setFormatter(format)

    logger.handlers = [handler]
    return logger


class DefaultLogger():
    """ Class providing log method which logs to stdout. """

    def __init__(self, level=_DEFAULT_LEVEL):
        """ Initializes a logging.Logger instance with given level

        Args:
            level (int): Minimum logging level
        """

        self.logger = update_logger(__name__, level=level)
        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.LOG_LEVEL_SET.format(
                file=FileNameEnum.Logger,
                level=level
            )
        )


class Logger(singleton.Singleton):
    """ Singleton class to provide unique logger instance among all modules. """

    def __init__(self, logger=None):
        """ Initializes singleton Logger with a logger instance.

        Args:
            logger (vwo.logger.SimpleLogger|
                    logging.Logger|
                    CustomLogger|
                    None): A logger instance
        """

        if not logger:
            self.logger = update_logger(__name__)
        elif isinstance(logger, DefaultLogger):
            self.logger = logger.logger
        elif validate_util.is_valid_utility(logger, 'logger'):
            try:
                logger.log(
                    LogLevelEnum.DEBUG,
                    LogMessageEnum.DEBUG_MESSAGES.CUSTOM_LOGGER_USED.format(
                        file=FileNameEnum.Logger
                    )
                )
                self.logger = logger
            except Exception:
                self.logger = update_logger(__name__)
                self.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.CUSTOM_LOGGER_MISCONFIGURED.
                    format(
                        file=FileNameEnum.Logger,
                        extra_info='log method is invalid.'
                    )
                )
        else:
            self.logger = update_logger(__name__)
            self.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CUSTOM_LOGGER_MISCONFIGURED.
                format(
                    file=FileNameEnum.Logger,
                    extra_info='log method is not provided.'
                )
            )

    def log(self, level, message):
        """ Log method which takes two parameters and logs the message according to
        handler of logger provided while instantiating this class.

        Args:
            level (int): Level of log
            message (string): Message to log
        """

        try:
            self.logger.log(level, message)
        except Exception:
            # Even logging.Logger is broken somehow, simply print to console
            print(level, message)
