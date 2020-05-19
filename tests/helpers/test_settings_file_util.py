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

import mock
import unittest
import random
from requests import exceptions as request_exception
import sys
from vwo import get_settings_file
from vwo.constants import constants
from ..data.constants import TEST_SDK_KEY, TEST_ACCOUNT_ID

if sys.version_info[0] < 3:
    from io import BytesIO as StringIO
else:
    from io import StringIO


class SettingsFileTest(unittest.TestCase):
    def test_get_settings_file_fires_request(self):
        """ Test that get_settings_file fires off requests call with
        provided account_id and sdk_key. """
        default_random = random.random

        def dummy_random():
            return 0.05353966086631112

        random.random = dummy_random
        with mock.patch("requests.get") as mock_request_get:
            mock_request_get.return_value.status_code = 200
            mock_request_get.return_value.text = "dummy_setting_file"
            result = get_settings_file(TEST_ACCOUNT_ID, "TEST_SDK_KEY")
            self.assertEqual(result, "dummy_setting_file")

        url = "https://dev.visualwebsiteoptimizer.com/server-side/settings"
        params = {
            "a": TEST_ACCOUNT_ID,
            "i": "TEST_SDK_KEY",
            "api-version": constants.API_VERSION,
            "r": 0.05353966086631112,
            "platform": constants.PLATFORM,
        }
        mock_request_get.assert_called_once_with(url, params=params)
        random.random = default_random

    def test_get_settings_file_error_status_code(self):
        """ Test that get_settings_file returns None if status_code != 200. """
        default_random = random.random

        def dummy_random():
            return 0.05353966086631112

        random.random = dummy_random
        with mock.patch("requests.get") as mock_request_get, mock.patch("sys.stderr", new=StringIO()) as fakeOutput:
            mock_request_get.return_value.status_code = 503
            mock_request_get.return_value.text = '{"message":"Invalid api key"}'
            result = get_settings_file(TEST_ACCOUNT_ID, "TEST_SDK_KEY")
            self.assertEqual(result, '{"message":"Invalid api key"}')
            self.assertEqual(
                fakeOutput.getvalue().strip(),
                'Request failed for fetching account settings. Got Status Code: 503 and message: {"message":"Invalid api key"}.',  # noqa: E501
            )
        random.random = default_random

    def test_get_settings_with_exception(self):
        """ Test that get_settings_file raises exception. """
        default_random = random.random

        def dummy_random():
            return 0.05353966086631112

        random.random = dummy_random
        with mock.patch(
            "requests.get", side_effect=request_exception.RequestException("Failed Request")
        ) as mock_request_get, mock.patch("sys.stderr", new=StringIO()) as fakeOutput:
            result = get_settings_file(TEST_ACCOUNT_ID, "TEST_SDK_KEY")
            self.assertEqual(result, "{}")
            self.assertEqual(fakeOutput.getvalue().strip(), "Error fetching Settings File Failed Request")

        url = "https://dev.visualwebsiteoptimizer.com/server-side/settings"
        params = {
            "a": TEST_ACCOUNT_ID,
            "i": "TEST_SDK_KEY",
            "api-version": constants.API_VERSION,
            "r": 0.05353966086631112,
            "platform": constants.PLATFORM,
        }
        mock_request_get.assert_called_once_with(url, params=params)
        random.random = default_random

    def test_empty_account_id_return_none(self):
        result = get_settings_file("", TEST_SDK_KEY)
        self.assertEqual(result, "{}")

    def test_empty_sdk_key_return_none(self):
        result = get_settings_file(TEST_ACCOUNT_ID, "")
        self.assertEqual(result, "{}")
