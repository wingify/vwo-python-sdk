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
import unittest
import json
import random
import mock

import vwo
from ..data.settings_files import SETTINGS_FILES 
from ..data.constants import TEST_ACCOUNT_ID, TEST_SDK_KEY

from ..config.config import TEST_LOG_LEVEL


class GetAndUpdateSettingsFileTest(unittest.TestCase):
    def set_up(self, config_variant="AB_T_100_W_0_100"):
        self.user_id = str(random.random())
        self.settings_file = json.dumps(SETTINGS_FILES.get(config_variant))

        self.vwo = vwo.launch(self.settings_file, is_development_mode=True, log_level=TEST_LOG_LEVEL)
        self.campaign_key = config_variant
        try:
            self.goal_identifier = SETTINGS_FILES[config_variant]["campaigns"][0]["goals"][0]["identifier"]
        except Exception:
            pass
    
    def test_invalid_args_passed(self):
        self.set_up()
        result = self.vwo.get_and_update_settings_file("", "")
        self.assertEqual(result, self.settings_file)

    def test_invalid_account_id_passed(self):
        self.set_up()
        result = self.vwo.get_and_update_settings_file("", TEST_SDK_KEY)
        self.assertEqual(result, self.settings_file)

    def test_invalid_sdk_key_passed(self):
        self.set_up()
        result = self.vwo.get_and_update_settings_file(TEST_ACCOUNT_ID, "")
        self.assertEqual(result, self.settings_file)
    
    def test_invalid_settings_file_fetched(self):
        self.set_up()
        with mock.patch("vwo.services.settings_file_manager.get_settings_file", return_value="{}"):
            result = self.vwo.get_and_update_settings_file(TEST_ACCOUNT_ID, TEST_SDK_KEY)
            self.assertEqual(result, self.settings_file)

    def test_same_settings_file_fetched(self):
        self.set_up()
        with mock.patch("vwo.services.settings_file_manager.get_settings_file", return_value=self.settings_file):       
            result = self.vwo.get_and_update_settings_file(TEST_ACCOUNT_ID, TEST_SDK_KEY)
            self.maxDiff = None
            self.assertEqual(result, self.settings_file)

    def test_updated_settings_file_fetched(self):
        self.set_up()
        config_variant = "AB_T_100_W_50_50"
        with mock.patch("vwo.services.settings_file_manager.get_settings_file", return_value=json.dumps(SETTINGS_FILES.get(config_variant))):       
            result = self.vwo.get_and_update_settings_file(TEST_ACCOUNT_ID, TEST_SDK_KEY)
            self.maxDiff = None
            self.assertEqual(result, json.dumps(SETTINGS_FILES.get(config_variant)))