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

from vwo.enums.file_name_enum import FileNameEnum
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

    def test_is_valid_batch_event_settings_events_per_request_passed_below_limit(self):
        val = {
            'events_per_request': 0
        }
        result = validate_util.is_valid_batch_event_settings(val, FileNameEnum.Api.Launch)
        self.assertIs(result, False)

    def test_is_valid_batch_event_settings_events_per_request_passed_above_limit(self):
        val = {
            'events_per_request': 5001
        }
        result = validate_util.is_valid_batch_event_settings(val, FileNameEnum.Api.Launch)
        self.assertIs(result, False)

    def test_is_valid_batch_event_settings_events_per_request_passed_with_decimal(self):
        val = {
            'events_per_request': 400.2
        }
        result = validate_util.is_valid_batch_event_settings(val, FileNameEnum.Api.Launch)
        self.assertIs(result, False)

    def test_is_valid_batch_event_settings_request_time_interval_passed_with_character(self):
        val = {
            'request_time_interval': 'a'
        }
        result = validate_util.is_valid_batch_event_settings(val, FileNameEnum.Api.Launch)
        self.assertIs(result, False)

    def test_is_valid_batch_event_settings_request_time_interval_below_limit(self):
        val = {
            'request_time_interval': 0.2
        }
        result = validate_util.is_valid_batch_event_settings(val, FileNameEnum.Api.Launch)
        self.assertIs(result, False)

    def test_is_valid_batch_event_settings_missing_values(self):
        val = {
            'flush_callback': 1
        }
        result = validate_util.is_valid_batch_event_settings(val, FileNameEnum.Api.Launch)
        self.assertIs(result, False)

    def test_is_valid_batch_event_settings_flush_callback_non_callable(self):
        val = {
            'events_per_request': 400,
            'request_time_interval': 10,
            'flush_callback': 1
        }
        result = validate_util.is_valid_batch_event_settings(val, FileNameEnum.Api.Launch)
        self.assertIs(result, False)

    def test_is_valid_batch_event_settings_non_dict(self):
        val = 1
        result = validate_util.is_valid_batch_event_settings(val, FileNameEnum.Api.Launch)
        self.assertIs(result, False)

