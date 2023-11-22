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

import json
import random
import unittest

import vwo
from ..data.settings_files import SETTINGS_FILES
from ..data.settings_file_and_user_expectations import USER_EXPECTATIONS


class test_mutually_exclusive_newimpl(unittest.TestCase):
    def setUp(self):
        # user ID
        self.user_id = str(random.random())

    # called campaign is same as priority campaign
    def test_called_campaign_is_priority_campaign(self):
        settings_file = SETTINGS_FILES["SETTINGS_MEGNEW_ONLY_PRIORITY"]
        vwo_instance = vwo.launch(json.dumps(settings_file))
        user_and_variations = USER_EXPECTATIONS["SETTINGS_MEGNEW_ONLY_PRIORITY"]
        campaign_key = settings_file.get("campaigns")[0].get("key")

        # get variation for each test user and validate
        for test in user_and_variations:
            variation = vwo_instance.get_variation_name(campaign_key, test["user"])
            self.assertEqual(variation, test["variation"])

    # called campaign is not same as priority campaign
    def test_called_campaign_is_not_priority_campaign(self):
        settings_file = SETTINGS_FILES["SETTINGS_MEGNEW_ONLY_PRIORITY"]
        vwo_instance = vwo.launch(json.dumps(settings_file))
        user_and_variations = USER_EXPECTATIONS["SETTINGS_MEGNEW_ONLY_PRIORITY"]
        campaign_key = settings_file.get("campaigns")[1].get("key")

        # get variation for each test user and validate
        for test in user_and_variations:
            variation = vwo_instance.get_variation_name(campaign_key, test["user"])
            self.assertIsNone(variation)

    # traffic weightage campaigns
    def test_traffic_weightage_campaigns(self):
        settings_file = SETTINGS_FILES["SETTINGS_MEGNEW_ONLY_TRAFFIC"]
        vwo_instance = vwo.launch(json.dumps(settings_file))

        # high and low traffic campaigns
        high_traffic_campaign_key = settings_file.get("campaigns")[0].get("key")
        low_traffic_campaign_key = settings_file.get("campaigns")[1].get("key")

        # count for returned valid variations
        high_traffic_count = 0
        low_traffic_count = 0

        # run through 1000 iterations of called campaign is high traffic campaign
        for i in range(1000):
            user_id = "user" + str(i)
            # call activate on local vwo instance and get variation
            variation = vwo_instance.get_variation_name(high_traffic_campaign_key, user_id)

            # if valid variation returned, increment high count
            if variation:
                high_traffic_count += 1

        # run through 1000 iterations of called campaign is low traffic campaign
        for i in range(1000):
            user_id = "user" + str(i)
            # call activate on local vwo and get variation
            variation = vwo_instance.get_variation_name(low_traffic_campaign_key, user_id)

            # if valid variation returned, increment low count
            if variation:
                low_traffic_count += 1

        # check that campaigns returned variation within a tolerance of 5% (high is 80%, low is 20%)
        self.assertAlmostEqual(high_traffic_count, 800, delta=50)
        self.assertAlmostEqual(low_traffic_count, 200, delta=50)
