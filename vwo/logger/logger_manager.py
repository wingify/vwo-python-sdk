from __future__ import print_function
import logging
from ..helpers import validate_util
from ..services import singleton
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from logging import DEBUG, INFO, WARNING, ERROR


_VWO_LOG_FORMAT = 'VWO-SDK - [%(levelname)s]: %(asctime)s %(message)s'
_DEFAULT_LOGGING_LEVEL = logging.ERROR


def set_log_level(logger, level):
    logger.setLevel(level)


def set_log_handler(logger, handler):
    logger.handlers = [handler]


def configure_logger(name=__name__, level=_DEFAULT_LOGGING_LEVEL, handler=logging.StreamHandler()):
    """ Creates a new logger instance with given name if it does not
    exists, else retrives existing logger. Then it configures logging.Logger
    instance recieved with given level and handler.

    Args:
        name (string): constant name for logger
        level (int): numerical value of level usually between, 0 to 50
        handler (logging.handlers): a handler logger instance

    Returns:
        logging.Logger: A logging.Logger object
    """
    # Set log format
    try:
        handler.setFormatter(logging.Formatter(_VWO_LOG_FORMAT))
    except Exception:
        # Unable to set format to custom handler
        pass

    # Retrieve logger instance
    logger = logging.getLogger(name)

    # Set logger level
    set_log_level(logger, level)

    # Set logger handler
    set_log_handler(logger, handler)

    # Log logger configured with level
    logger.log(
        DEBUG,
        LogMessageEnum.DEBUG_MESSAGES.LOG_LEVEL_SET.format(
            file=FileNameEnum.LoggerManager,
            level=level
        )
    )
    return logger


# For exposing log levels to vwo_instance
class LogLevels:
    DEBUG = DEBUG
    INFO = INFO
    WARNING = WARNING
    ERROR = ERROR


# VWO singleton Logger
class VWOLogger(singleton.Singleton):
    """ Singleton logger class to provide unique logger instance among all modules. """

    def __init__(self, logger=None):
        """ Initializes singleton Logger with a logger instance.

        Args:
            logger (vwo.logger.logger.SimpleLogger|
                    logging.Logger|
                    CustomLogger|
                    None): A logger instance
        """

        if not logger:
            # simply log to stdout
            self.logger = configure_logger(__name__)
        elif validate_util.is_valid_service(logger, 'logger'):
            try:
                logger.log(
                    DEBUG,
                    LogMessageEnum.DEBUG_MESSAGES.CUSTOM_LOGGER_USED.format(
                        file=FileNameEnum.LoggerManager
                    )
                )
                self.logger = logger
            except Exception:
                self.logger = configure_logger(__name__)
                self.log(
                    ERROR,
                    LogMessageEnum.ERROR_MESSAGES.CUSTOM_LOGGER_MISCONFIGURED.
                    format(
                        file=FileNameEnum.LoggerManager,
                        extra_info='log method is invalid.'
                    )
                )
        else:
            self.logger = configure_logger(__name__)
            self.log(
                ERROR,
                LogMessageEnum.ERROR_MESSAGES.CUSTOM_LOGGER_MISCONFIGURED.
                format(
                    file=FileNameEnum.LoggerManager,
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
