import unittest
import json

from vwo.helpers import validate_util
from ..data.settings_files import SETTINGS_FILES


class ValidatorTest(unittest.TestCase):

    def test_is_valid_settings_file_return_false(self):
        result = validate_util.is_valid_settings_file('')
        self.assertIs(result, False)

    def test_is_valid_settings_file_return_true(self):
        result = validate_util.is_valid_settings_file(
            json.dumps(SETTINGS_FILES['AB_T_100_W_50_50']))
        self.assertIs(result, True)

    def test_utility_validator(self):
        class InvalidUtility:
            pass
        result = validate_util.is_valid_service(InvalidUtility,
                                                'InvalidUtility')
        self.assertIs(result, False)
