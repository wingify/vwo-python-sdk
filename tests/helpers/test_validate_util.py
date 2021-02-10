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

import unittest
import json
import sys

from vwo.helpers import validate_util
from ..data.settings_files import SETTINGS_FILES


class ValidateUtilTest(unittest.TestCase):
    def test_is_valid_settings_file_return_false(self):
        result = validate_util.is_valid_settings_file("")
        self.assertIs(result, False)

    def test_is_valid_settings_file_return_true(self):
        result = validate_util.is_valid_settings_file(json.dumps(SETTINGS_FILES["AB_T_100_W_50_50"]))
        self.assertIs(result, True)

    def test_is_valid_settings_file_int_passed(self):
        result = validate_util.is_valid_settings_file(1)
        self.assertIs(result, False)

    def test_is_valid_settings_file_invalid_dict_passed(self):
        result = validate_util.is_valid_settings_file(json.dumps('{"a":1}'))
        self.assertIs(result, False)

    def test_utility_validate_util(self):
        class InvalidUtility:
            pass

        result = validate_util.is_valid_service(InvalidUtility, "InvalidUtility")
        self.assertIs(result, False)

    def test_is_valid_unicode_true(self):
        if sys.version_info[0] < 3:
            val = u"some_value"
            self.assertIs(True, validate_util.is_valid_unicode(val))

    def test_is_valid_unicode_false(self):
        if sys.version_info[0] < 3:
            val = "some_value"
            self.assertIs(False, validate_util.is_valid_unicode(val))
