# Copyright 2019 Wingify Software Pvt. Ltd.
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

from vwo.logger.logger_manager import VWOLogger, configure_logger
from vwo.services import singleton


class LoggerTest(unittest.TestCase):
    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_no_logger_passed(self):
        logger_instance = VWOLogger.getInstance()
        self.assertIsInstance(logger_instance.logger, logging.Logger)
        self.assertEqual(logger_instance.logger.level, logging.ERROR)

    def test_valid_custom_logger(self):
        class CustomLogger:
            def log(self, level, message):
                pass

        logger_instance = VWOLogger.getInstance(CustomLogger())
        self.assertIsInstance(logger_instance.logger, CustomLogger)

    def test_invalid_custom_logger(self):
        class CustomLogger:
            def log(self):
                pass

        logger_instance = VWOLogger.getInstance(CustomLogger())
        self.assertIsInstance(logger_instance.logger, logging.Logger)

    def test_custom_logger_with_no_log_passed(self):
        class CustomLogger:
            pass
        logger_instance = VWOLogger.getInstance(CustomLogger())
        self.assertIsInstance(logger_instance.logger, logging.Logger)

    def test_logging_logger_passed_with_broken_log(self):

        # Test logger is working normally
        default_logger = configure_logger(level=logging.INFO)
        logger_instance = VWOLogger.getInstance(default_logger)
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

        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            logger_instance.log(logging.ERROR, 'This logger instance used print for log')  # noqa: 501
            self.assertEqual(fakeOutput.getvalue().strip(),
                             str(logging.ERROR) + ' ' + 'This logger instance used print for log')  # noqa: 501

        logger_instance.logger.log = default_logging_logger
