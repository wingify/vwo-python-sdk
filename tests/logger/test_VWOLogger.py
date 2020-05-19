# Copyright 2019-2020 Wingify Software Pvt. Ltd.
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

import unittest
import logging
from mock import patch
import sys

from vwo.logger import VWOLogger


class VWOLoggerTest(unittest.TestCase):
    def tearDown(self):
        VWOLogger.clearExistingLoggerInstance()

    def test_no_logger_passed(self):
        logger_instance = VWOLogger.getInstance()
        self.assertIsInstance(logger_instance.logger, logging.Logger)
        self.assertEqual(logger_instance.logger.level, logging.ERROR)

    def test_valid_custom_logger(self):
        class CustomLogger:
            def log(self, level, message):
                pass

        logger_instance = VWOLogger.getInstance(logger=CustomLogger())
        self.assertIsInstance(logger_instance.logger, CustomLogger)

    def test_invalid_custom_logger(self):
        class CustomLogger:
            def log(self):
                pass

        logger_instance = VWOLogger.getInstance(logger=CustomLogger())
        self.assertIsInstance(logger_instance.logger, logging.Logger)

    def test_custom_logger_with_no_log_passed(self):
        class CustomLogger:
            pass

        logger_instance = VWOLogger.getInstance(logger=CustomLogger())
        self.assertIsInstance(logger_instance.logger, logging.Logger)

    def test_logging_logger_passed_with_broken_log(self):

        # Test logger is working normally
        default_logger = VWOLogger.create_console_logger(level=logging.INFO)
        logger_instance = VWOLogger.getInstance(logger=default_logger)
        self.assertIsInstance(logger_instance.logger, logging.Logger)
        self.assertEqual(logger_instance.logger.level, logging.INFO)

        default_logging_logger = logger_instance.logger.log

        # Break the log method
        def dummy_log_method():
            pass

        logger_instance.logger.log = dummy_log_method

        # Test whether the logger_instance prints to stdout or not

        if sys.version_info[0] < 3:
            from io import BytesIO as StringIO
        else:
            from io import StringIO

        with patch("sys.stdout", new=StringIO()) as fakeOutput:
            logger_instance.log(logging.ERROR, "This logger instance used print for log")  # noqa: 501
            self.assertEqual(
                fakeOutput.getvalue().strip(), str(logging.ERROR) + " " + "This logger instance used print for log",
            )  # noqa: 501

        logger_instance.logger.log = default_logging_logger

    def test_create_console_logger_None_level_passed(self):
        logger = VWOLogger.create_console_logger(level=None)
        self.assertEquals(logger.level, logging.ERROR)

    def test_create_console_logger_nothing_passed(self):
        logger = VWOLogger.create_console_logger()
        self.assertEquals(logger.level, logging.ERROR)

    def test_set_api(self):
        logger_instance = VWOLogger.getInstance()
        logger_instance.set_api("ACTIVATE")
        self.assertEquals(logger_instance.api_name, "ACTIVATE")

    def test_clearExistingLoggerInstance(self):
        logger = VWOLogger.getInstance()
        self.assertIsInstance(logger, VWOLogger.VWOLogger)
        VWOLogger.clearExistingLoggerInstance()
        self.assertIsNone(VWOLogger._logger)

    def test_getInstance_nothing_passed(self):
        logger = VWOLogger.getInstance()
        self.assertIsInstance(logger, VWOLogger.VWOLogger)
        self.assertIs(logger.logger.level, 40)

    def test_getInstance_log_level_passed(self):
        logger = VWOLogger.getInstance(log_level=20)
        self.assertIsInstance(logger, VWOLogger.VWOLogger)
        self.assertIs(logger.logger.level, 20)

    def test_getInstance_logging_logger_passed(self):
        logger = VWOLogger.getInstance(logger=logging.getLogger())
        self.assertIsInstance(logger, VWOLogger.VWOLogger)
        self.assertIs(logger.logger.level, 30)  # Default log level of logging.Logger is INFO, ie 30

    def test_getInstance_custom_logger_passed(self):
        class Logger:
            def log(self, *args):
                pass

        logger = VWOLogger.getInstance(logger=Logger())
        self.assertIsInstance(logger, VWOLogger.VWOLogger)
        self.assertIsInstance(logger.logger, Logger)

    def test_getInstance_broken_logger_passed(self):
        class Logger:
            def log(self):
                pass

        logger = VWOLogger.getInstance(logger=Logger())
        self.assertIsInstance(logger, VWOLogger.VWOLogger)
        self.assertIsInstance(logger.logger, logging.Logger)

    def test_getInstance_called_twice_with_kwargs(self):
        logger = VWOLogger.getInstance(log_level=20)
        self.assertIsInstance(logger, VWOLogger.VWOLogger)
        with self.assertRaises(Exception):
            VWOLogger.getInstance(log_level=20)

    def test_re_initialization_of_logger(self):
        logger = VWOLogger.getInstance()
        self.assertIsInstance(logger, VWOLogger.VWOLogger)
        # should raise exception as logger is not cleared
        with self.assertRaises(Exception):
            VWOLogger.getInstance(log_level=20)
        # should make private logger None
        VWOLogger.clearExistingLoggerInstance()
        self.assertIsNone(VWOLogger._logger)
        # re-initializing logger with passed logger object should succeed now
        logging_logger = logging.getLogger()
        logger = VWOLogger.getInstance(logger=logging_logger)
        self.assertIsInstance(logger, VWOLogger.VWOLogger)
        self.assertIsInstance(logger.logger, logging.Logger)
