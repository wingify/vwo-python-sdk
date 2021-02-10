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
import random
import copy
from vwo.core import bucketer
from vwo.helpers import campaign_util
from ..data.settings_files import SETTINGS_FILES
from ..data.settings_file_and_user_expectations import USER_EXPECTATIONS


class BucketerTest(unittest.TestCase):
    def setUp(self):

        self.user_id = str(random.random())
        self.dummy_campaign = {
            "goals": [{"identifier": "GOAL_NEW", "id": 203, "type": "CUSTOM_GOAL"}],
            "variations": [
                {"id": "1", "name": "Control", "weight": 40},
                {"id": "2", "name": "Variation-1", "weight": 60},
            ],
            "id": 22,
            "percentTraffic": 50,
            "key": "UNIQUE_KEY",
            "status": "RUNNING",
            "type": "VISUAL_AB",
        }
        campaign_util.set_variation_allocation(self.dummy_campaign)
        self.bucketer = bucketer.Bucketer()
        self.variations = copy.deepcopy(SETTINGS_FILES["FT_T_0_W_10_20_30_40"].get("campaigns")[0]["variations"])
        variation_allocations = campaign_util.get_variation_allocation_ranges(self.variations)
        campaign_util.set_variation_allocation_from_ranges(self.variations, variation_allocations)

    def test_user_part_of_campaign_none_campaign_passed(self):
        result = self.bucketer.is_user_part_of_campaign(self.user_id, None)
        self.assertIs(result, False)

    def test_user_part_of_campaign_none_userid_passed(self):
        result = self.bucketer.is_user_part_of_campaign(None, self.dummy_campaign)
        self.assertIs(result, False)

    def test_user_part_of_campaign_should_return_true(self):
        user_id = "Bob"
        # Bob, with above campaign settings, will get hashValue:2033809345 and
        # bucketValue:48. So, MUST be a part of campaign as per campaign
        # percentTraffic
        result = self.bucketer.is_user_part_of_campaign(user_id, self.dummy_campaign)
        self.assertIs(result, True)

    def test_user_part_of_campaign_should_return_false(self):
        user_id = "Lucian"
        # Lucian, with above campaign settings, will get hashValue:2251780191
        # and bucketValue:53. So, must NOT be a part of campaign as per campaign
        # percentTraffic
        result = self.bucketer.is_user_part_of_campaign(user_id, self.dummy_campaign)
        self.assertIs(result, False)

    def test_user_part_of_campaign_should_return_false_as_T_is_0(self):
        campaign = copy.deepcopy(self.dummy_campaign)
        campaign["percentTraffic"] = 0
        for test in USER_EXPECTATIONS["AB_T_50_W_50_50"]:
            self.assertIs(False, self.bucketer.is_user_part_of_campaign(test["user"], campaign))

    def test_user_part_of_campaign_should_return_true_as_T_is_100(self):
        campaign = copy.deepcopy(self.dummy_campaign)
        campaign["percentTraffic"] = 100
        for test in USER_EXPECTATIONS["AB_T_50_W_50_50"]:
            self.assertIs(True, self.bucketer.is_user_part_of_campaign(test["user"], campaign))

    def test_user_part_of_campaign_AB_T_50_W_50_50(self):
        campaign = copy.deepcopy(SETTINGS_FILES["AB_T_50_W_50_50"]["campaigns"][0])
        for test in USER_EXPECTATIONS["AB_T_50_W_50_50"]:
            self.assertIs(test["variation"] is not None, self.bucketer.is_user_part_of_campaign(test["user"], campaign))

    def test_user_part_of_campaign_T_25_W_10_20_30_40(self):
        campaign = copy.deepcopy(SETTINGS_FILES["FT_T_25_W_10_20_30_40"]["campaigns"][0])
        for test in USER_EXPECTATIONS["T_25_W_10_20_30_40"]:
            self.assertIs(test["variation"] is not None, self.bucketer.is_user_part_of_campaign(test["user"], campaign))

    def test_bucket_user_to_variation_none_campaign_passed(self):
        result = self.bucketer.bucket_user_to_variation(self.user_id, None)
        self.assertIsNone(result)

    def test_bucket_user_to_variation_none_userid_passed(self):
        result = self.bucketer.bucket_user_to_variation(None, self.dummy_campaign)
        self.assertIsNone(result)

    def test_bucket_user_to_variation_return_control(self):
        user_id = "Sarah"
        # Sarah, with above campaign settings, will get hashValue:69650962 and
        # bucketValue:326. So, MUST be a part of Control, as per campaign
        # settings
        result = self.bucketer.bucket_user_to_variation(user_id, self.dummy_campaign)
        self.assertEqual(result.get("name"), "Control")

    def test_bucket_user_to_variation_return_variation_1(self):
        user_id = "Varun"
        # Varun, with above campaign settings, will get hashValue:69650962 and
        # bucketValue:326. So, MUST be a part of Variation-1, as per campaign
        # settings
        result = self.bucketer.bucket_user_to_variation(user_id, self.dummy_campaign)
        self.assertEqual(result.get("name"), "Variation-1")

    def test_bucket_user_to_variation_should_return_true(self):
        user_id = "Allie"
        # Allie, with above campaign settings, will get hashValue:362121553
        # and bucketValue:1688. So, MUST be a part of campaign as per campaign
        # percentTraffic
        variation = self.bucketer.bucket_user_to_variation(user_id, self.dummy_campaign)
        self.assertEqual(variation.get("id"), "1")
        self.assertEqual(variation.get("name"), "Control")

    def test_bucket_user_to_variation_should_return_none(self):
        user_id = "Lucian"
        # Lucian, with above campaign settings, will get hashValue:2251780191
        # and bucketValue:53. So, MUST be a part of campaign as per campaign
        # percentTraffic
        variation = self.bucketer.bucket_user_to_variation(user_id, self.dummy_campaign)
        self.assertIsNone(variation)

    def test_bucket_user_to_variation_should_return_Control(self):
        user_id = "Sarah"
        # Sarah, with above campaign settings, will get hashValue:69650962
        # and bucketValue:326. So, MUST be a part of Control, as per campaign
        # settings
        variation = self.bucketer.bucket_user_to_variation(user_id, self.dummy_campaign)
        self.assertEqual(variation.get("name"), "Control")

    def test_bucket_user_to_variation_should_return_Variation(self):
        user_id = "Varun"
        # Varun, with above campaign settings, will get hashValue:2025462540
        # and bucketValue:9433. So, MUST be a part of Variation, as per campaign
        # settings
        variation = self.bucketer.bucket_user_to_variation(user_id, self.dummy_campaign)
        self.assertEqual(variation.get("name"), "Variation-1")

    def test_get_variation_return_control_below_border(self):
        variation = self.bucketer.get_variation(self.variations, 999)
        self.assertEquals(variation.get("name"), "Control")

    def test_get_variation_return_control_border(self):
        variation = self.bucketer.get_variation(self.variations, 1000)
        self.assertEquals(variation.get("name"), "Control")

    def test_get_variation_return_variation_1_above_border(self):
        variation = self.bucketer.get_variation(self.variations, 1001)
        self.assertEquals(variation.get("name"), "Variation-1")

    def test_get_variation_return_variation_1(self):
        variation = self.bucketer.get_variation(self.variations, 3000)
        self.assertEquals(variation.get("name"), "Variation-1")

    def test_get_variation_return_variation_2(self):
        variation = self.bucketer.get_variation(self.variations, 6000)
        self.assertEquals(variation.get("name"), "Variation-2")

    def test_get_variation_return_variation_3(self):
        variation = self.bucketer.get_variation(self.variations, 10000)
        self.assertEquals(variation.get("name"), "Variation-3")

    def test_get_variation_return_none(self):
        variation = self.bucketer.get_variation(self.variations, 10001)
        self.assertIsNone(variation)

    def test_get_bucket_value_for_multiple_user_ids(self):
        for test in USER_EXPECTATIONS["USER_AND_BUCKET_VALUES"]:
            bucket_value = self.bucketer.get_bucket_value_for_user(test["user"], 10000)
            self.assertEquals(bucket_value, test["bucket_value"])

    def test_get_bucket_value_for_user_64(self):
        bucket_value = self.bucketer.get_bucket_value_for_user("someone@mail.com", 100)
        self.assertEquals(bucket_value, 64)

    def test_get_bucket_value_for_user_50(self):
        bucket_value = self.bucketer.get_bucket_value_for_user("1111111111111111", 100)
        self.assertEquals(bucket_value, 50)
