# Copyright 2019-2022 Wingify Software Pvt. Ltd.
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
from ..data.settings_files import SETTINGS_FILES
from ..data.settings_file_and_user_expectations import USER_EXPECTATIONS
import json
import vwo


class BucketerNewTest(unittest.TestCase):
    def setUp(self):
        self.log_level = vwo.LOG_LEVELS.DEBUG

    def test_settings_without_seed_without_isOB(self):
        settings_file = SETTINGS_FILES["SETTINGS_WITHOUT_SEED_WITHOUT_ISOB"]
        vwo_instance = vwo.launch(json.dumps(settings_file))
        user_and_variations = USER_EXPECTATIONS["SETTINGS_WITHOUT_SEED_WITHOUT_ISOB"]
        campaign_key = settings_file.get("campaigns")[0].get("key")

        # parse through the user/variation combination and verify results
        for test in user_and_variations:
            variation = vwo_instance.get_variation_name(campaign_key, test["user"])
            self.assertEqual(variation, test["variation"])

    def test_settings_with_seed_without_isOB(self):
        settings_file = SETTINGS_FILES["SETTINGS_WITH_SEED_WITHOUT_ISOB"]
        vwo_instance = vwo.launch(json.dumps(settings_file))
        user_and_variations = USER_EXPECTATIONS["SETTINGS_WITH_SEED_WITHOUT_ISOB"]
        campaign_key = settings_file.get("campaigns")[0].get("key")

        # parse through the user/variation combination and verify results
        for test in user_and_variations:
            variation = vwo_instance.get_variation_name(campaign_key, test["user"])
            self.assertEqual(variation, test["variation"])

    def test_settings_with_isNB_with_isOB(self):
        settings_file = SETTINGS_FILES["SETTINGS_WITH_ISNB_WITH_ISOB"]
        vwo_instance = vwo.launch(json.dumps(settings_file))
        user_and_variations = USER_EXPECTATIONS["SETTINGS_WITH_ISNB_WITH_ISOB"]
        campaign_key = settings_file.get("campaigns")[0].get("key")

        # parse through the user/variation combination and verify results
        for test in user_and_variations:
            variation = vwo_instance.get_variation_name(campaign_key, test["user"])
            self.assertEqual(variation, test["variation"])

    def test_settings_with_isNB_without_isOB(self):
        settings_file = SETTINGS_FILES["SETTINGS_WITH_ISNB_WITHOUT_ISOB"]
        vwo_instance = vwo.launch(json.dumps(settings_file))
        user_and_variations = USER_EXPECTATIONS["SETTINGS_WITH_ISNB_WITHOUT_ISOB"]
        campaign_key = settings_file.get("campaigns")[0].get("key")

        # parse through the user/variation combination and verify results
        for test in user_and_variations:
            variation = vwo_instance.get_variation_name(campaign_key, test["user"])
            self.assertEqual(variation, test["variation"])

    def test_settings_without_seed_with_isNB_without_isOB(self):
        settings_file = SETTINGS_FILES["SETTINGS_WITHOUT_SEED_WITH_ISNB_WITHOUT_ISOB"]
        vwo_instance = vwo.launch(json.dumps(settings_file))
        user_and_variations = USER_EXPECTATIONS["SETTINGS_WITHOUT_SEED_WITH_ISNB_WITHOUT_ISOB"]
        campaign_key = settings_file.get("campaigns")[0].get("key")

        # parse through the user/variation combination and verify results
        for test in user_and_variations:
            variation = vwo_instance.get_variation_name(campaign_key, test["user"])
            self.assertEqual(variation, test["variation"])
