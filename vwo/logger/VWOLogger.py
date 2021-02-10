# Copyright 2019-2021 Wingify Software Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
import logging


_VWO_LOG_FORMAT = "VWO-SDK - [%(levelname)s]: %(asctime)s %(message)s"
API_NAME = "SDK"
_DEFAULT_LOGGING_LEVEL = logging.ERROR
FILE = FileNameEnum.Logger.LoggerManager
_logger = None


def clearExistingLoggerInstance():
    """ Clears the existing logger """
    global _logger
    _logger = None


def getInstance(**kwargs):
    """ Always use this method to get an instance of VWOLogger. Pass a valid log_level
    or logger object when calling for first time to instantiate a VWOLogger object.
    If logger is passed, log_level is neglected.
    It throws exception when called with kwargs 2nd time.

    Keyword Args:
        log_level (vwo.LOG_LEVELS): A valid log level accepted by this SDK
        logger (object): An object capable of logging events

    Returns:
        VWOLogger: Instance of a VWOLogger object
    """
    global _logger
    if _logger and kwargs:
        raise Exception("Initializing logger when it is already initialized")
    elif _logger:
        return _logger
    else:
        _logger = VWOLogger(**kwargs)
        return _logger


def create_console_logger(name=__name__, level=None):
    """ Creates a console logger with given name and level using python's standard logging module.

    Args:
        name (str): Name of the logger
        level (logging._levelNames): A logging level accepted by logger

    Returns:
        logging.Logger: A logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level or _DEFAULT_LOGGING_LEVEL)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(_VWO_LOG_FORMAT))
    logger.handlers = [handler]

    logger.log(
        logging.DEBUG,
        LogMessageEnum.DEBUG_MESSAGES.LOG_LEVEL_SET.format(file=FILE, level=level).replace("API_NAME", "SDK", 1),
    )
    return logger


class VWOLogger:
    """Module logger class to provide logging functionality. It accepts a logger object with
    log method in it or a log level to create default console logger"""

    def __init__(self, logger=None, log_level=None):
        """ Initializes VWOLogger with provided logger object or creates a console logger object
        with provided level.

        Args:
            logger (CustomLogger|logging.Logger|None): A logger object
            log_level (logging._levelNames): Level of log
        """
        # Set default api name as SDK
        self.api_name = API_NAME
        if logger:
            if isinstance(logger, logging.Logger):
                logger.log(
                    logging.DEBUG,
                    LogMessageEnum.DEBUG_MESSAGES.LOGGING_LOGGER_INSTANCE_USED.format(file=FILE).replace(
                        "API_NAME", self.api_name, 1
                    ),
                )
                self.logger = logger
            else:
                try:
                    logger.log(
                        logging.DEBUG,
                        LogMessageEnum.DEBUG_MESSAGES.CUSTOM_LOGGER_USED.format(file=FILE).replace(
                            "API_NAME", self.api_name, 1
                        ),
                    )
                    self.logger = logger
                except Exception:
                    self.logger = create_console_logger()
                    self.log(
                        logging.ERROR,
                        LogMessageEnum.ERROR_MESSAGES.CUSTOM_LOGGER_MISCONFIGURED.format(
                            file=FILE, extra_info="log method is not provided or invalid."
                        ).replace("API_NAME", self.api_name, 1),
                    )
        else:
            self.logger = create_console_logger(level=log_level)

    def set_api(self, api_name):
        """ It sets the api_name to the API currently being used, for logging purpose. """
        self.api_name = api_name

    def log(self, level, message):
        """ Log method which takes two parameters and logs the message according to
        handler of logger provided while instantiating this class.

        Args:
            level (int): Level of log
            message (string): Message to log
        """

        try:
            self.logger.log(level, message.replace("API_NAME", self.api_name, 1))
        except Exception:
            # Even logging.Logger is broken somehow, simply print to console
            print(level, message)
