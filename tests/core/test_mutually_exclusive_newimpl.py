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
from tests.config.config import TEST_LOG_LEVEL

with open("tests/data/mutually_exclusive_newimpl_test_cases.json") as mutually_exclusive_test_cases_json:
    new_meg_settings = json.load(mutually_exclusive_test_cases_json)


class test_mutually_exclusive_newimpl(unittest.TestCase):
    def setUp(self):
        # user ID
        self.user_id = str(random.random())

        # instantiate vwo instance
        settings_file = json.dumps(new_meg_settings)
        self.vwo_instance = vwo.launch(
            settings_file, log_level=TEST_LOG_LEVEL, user_storage=None, is_development_mode=True
        )

    # called campaign is same as priority campaign
    def test_called_campaign_is_priority_campaign(self):
        self.setUp()

        # get campaign details
        campaign = new_meg_settings["campaigns"][0]
        campaign_key = campaign["key"]

        # call activate and get variation
        variation = self.vwo_instance.activate(
            campaign_key,
            self.user_id,
        )

        # valid variation should be returned
        self.assertIsNotNone(variation)

    # called campaign is not priority campaign
    def test_called_campaign_is_not_priority_campaign(self):
        self.setUp()

        # get campaign details
        campaign = new_meg_settings["campaigns"][1]
        campaign_key = campaign["key"]

        # call activate and get variation
        variation = self.vwo_instance.activate(
            campaign_key,
            self.user_id,
        )

        # valid variation should not be returned
        self.assertIsNone(variation)

    # traffic weightage campaigns
    def test_traffic_weightage_campaigns(self):
        self.setUp()

        # high and low traffic campaigns
        high_traffic_campaign = new_meg_settings["campaigns"][2]
        low_traffic_campaign = new_meg_settings["campaigns"][3]
        high_traffic_campaign_key = high_traffic_campaign["key"]
        low_traffic_campaign_key = low_traffic_campaign["key"]

        # count for returned valid variations
        high_traffic_count = 0
        low_traffic_count = 0

        # remove priority from settings file and initialize local vwo instance (so that logic flows to traffic weightage)
        new_meg_settings_without_p = new_meg_settings
        # del new_meg_settings_without_p["groups"]["1"]["p"]
        new_meg_settings_without_p["groups"]["1"].pop("p", None)
        vwo_instance = vwo.launch(
            json.dumps(new_meg_settings_without_p),
            log_level=TEST_LOG_LEVEL,
            user_storage=None,
            is_development_mode=True,
        )

        # run through 1000 iterations of called campaign is high traffic campaign
        for _ in range(1000):
            # call activate on local vwo instance and get variation
            variation = vwo_instance.activate(high_traffic_campaign_key, self.user_id)

            # if valid variation returned, increment high count
            if variation:
                high_traffic_count += 1

        # run through 1000 iterations of called campaign is low traffic campaign
        for _ in range(1000):
            # call activate on local vwo and get variation
            variation = vwo_instance.activate(low_traffic_campaign_key, self.user_id)

            # if valid variation returned, increment low count
            if variation:
                low_traffic_count += 1

        # check that campaigns returned variation within a tolerance of 5% (high is 80%, low is 20%)
        self.assertAlmostEqual(high_traffic_count, 800, delta=50)
        self.assertAlmostEqual(low_traffic_count, 200, delta=50)
