import unittest
import logging
from mock import patch
import sys

from vwo import logger
from vwo.helpers import singleton


class LoggerTest(unittest.TestCase):
    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_no_logger_passed(self):
        logger_instance = logger.Logger.getInstance()
        self.assertIsInstance(logger_instance.logger, logging.Logger)
        self.assertEqual(logger_instance.logger.level, logging.ERROR)

    def test_default_logger_passed(self):
        default_logger = logger.DefaultLogger(logging.INFO)
        logger_instance = logger.Logger.getInstance(default_logger)
        self.assertIsInstance(logger_instance.logger, logging.Logger)
        self.assertEqual(logger_instance.logger.level, logging.INFO)

    def test_valid_custom_logger(self):
        class CustomLogger:
            def log(self, level, message):
                pass

        logger_instance = logger.Logger.getInstance(CustomLogger())
        self.assertIsInstance(logger_instance.logger, CustomLogger)

    def test_invalid_custom_logger(self):
        class CustomLogger:
            def log(self):
                pass

        logger_instance = logger.Logger.getInstance(CustomLogger())
        self.assertIsInstance(logger_instance.logger, logging.Logger)

    def test_custom_logger_with_no_log_passed(self):
        class CustomLogger:
            pass
        logger_instance = logger.Logger.getInstance(CustomLogger())
        self.assertIsInstance(logger_instance.logger, logging.Logger)

    def test_logging_logger_passed_with_broken_log(self):

        # Test logger is working normally
        default_logger = logger.DefaultLogger(logging.INFO)
        logger_instance = logger.Logger.getInstance(default_logger)
        self.assertIsInstance(logger_instance.logger, logging.Logger)
        self.assertEqual(logger_instance.logger.level, logging.INFO)

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
