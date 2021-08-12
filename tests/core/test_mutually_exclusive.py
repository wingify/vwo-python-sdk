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

import json
import random
import unittest

import vwo
from tests.config.config import TEST_LOG_LEVEL

with open("tests/data/mutually_exclusive_test_cases.json") as mutually_exclusive_test_cases_json:
    mutually_exclusive_test_cases = json.load(mutually_exclusive_test_cases_json)


class ClientUserStorage:
    def __init__(self):
        self.storage = {}

    def get(self, user_id, campaign_key):
        return self.storage.get((user_id, campaign_key))

    def set(self, user_data):
        self.storage[(user_data.get("userId"), user_data.get("campaignKey"))] = user_data
        return True


class MutuallyExclusiveTest(unittest.TestCase):
    def setUp(self):
        self.user_id = str(random.random())

    def set_up(self, case_id):
        _user_storage = ClientUserStorage()
        self.case = mutually_exclusive_test_cases.get(str(case_id))
        vwo_parameters = self.case.get("vwoParameters")

        settings_file = vwo_parameters.get("settingsFile")
        if not settings_file:
            settings_file = mutually_exclusive_test_cases.get("commonSettingsFile")
        self.settings_file = json.dumps(settings_file)

        self.user_storage = None
        if vwo_parameters.get("userStorageService"):
            self.user_storage = _user_storage

        self.user_id = self.case.get("userId")
        self.campaign_key = self.case.get("campaignKey")
        self.custom_variables = self.case.get("options").get("customVariables")
        self.variation_targeting_variables = self.case.get("options").get("variationTargetingVariables")
        self.vwo_instance = vwo.launch(
            self.settings_file, log_level=TEST_LOG_LEVEL, user_storage=self.user_storage, is_development_mode=True
        )

    def test_mutually_exclusive_case_1(self):
        self.set_up(1)

        variation = self.vwo_instance.activate(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )

        self.assertEqual(variation, self.case.get("expectation"), self.case.get("description"))

    def test_mutually_exclusive_case_2(self):
        self.set_up(2)

        variation = self.vwo_instance.activate(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertEqual(variation, self.case.get("expectation"), self.case.get("description"))

    def test_mutually_exclusive_case_3(self):
        self.set_up(3)

        variation = self.vwo_instance.activate(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertEqual(variation, self.case.get("expectation"), self.case.get("description"))

    def test_mutually_exclusive_case_4(self):
        self.set_up(4)

        variation = self.vwo_instance.activate(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertEqual(variation, self.case.get("expectation"), self.case.get("description"))

    def test_mutually_exclusive_case_5(self):
        self.set_up(5)

        variation = self.vwo_instance.activate(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertEqual(variation, self.case.get("expectation"), self.case.get("description"))
        self.assertEqual(
            self.user_storage.get(self.user_id, self.campaign_key).get("campaignKey"),
            self.campaign_key,
            self.case.get("description"),
        )

    def test_mutually_exclusive_case_6(self):
        self.set_up(6)

        variation = self.vwo_instance.activate(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertEqual(variation, self.case.get("expectation"), self.case.get("description"))

    def test_mutually_exclusive_case_7(self):
        self.set_up(7)

        is_feature_enabled = self.vwo_instance.is_feature_enabled(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )

        variation = self.vwo_instance.get_variation_name(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertListEqual(
            [is_feature_enabled, variation], self.case.get("expectation"), self.case.get("description")
        )

    def test_mutually_exclusive_case_8(self):
        self.set_up(8)

        is_feature_enabled = self.vwo_instance.is_feature_enabled(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        variation = self.vwo_instance.get_variation_name(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertListEqual(
            [is_feature_enabled, variation], self.case.get("expectation"), self.case.get("description")
        )

    def test_mutually_exclusive_case_9(self):
        self.set_up(9)

        is_feature_enabled = self.vwo_instance.is_feature_enabled(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        variation = self.vwo_instance.get_variation_name(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertListEqual(
            [is_feature_enabled, variation], self.case.get("expectation"), self.case.get("description")
        )

    def test_mutually_exclusive_case_10(self):
        self.set_up(10)

        is_feature_enabled = self.vwo_instance.is_feature_enabled(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        variation = self.vwo_instance.get_variation_name(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertListEqual(
            [is_feature_enabled, variation], self.case.get("expectation"), self.case.get("description")
        )

        variation = self.vwo_instance.activate(
            "c5",
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )

        self.assertEqual("Variation-1", variation, self.case.get("description"))

        # Adding c5 campaign as part of another group
        self.vwo_instance.config.settings_file.get("campaignGroups").update({"5": 1})
        self.vwo_instance.config.settings_file.get("groups").get("1").get("campaigns").append(5)
        self.vwo_instance.config.settings_file.get("groups").get("2").get("campaigns").remove(5)

        is_feature_enabled = self.vwo_instance.is_feature_enabled(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        variation = self.vwo_instance.get_variation_name(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        # winner campaign changed thus returned false
        self.assertListEqual([is_feature_enabled, variation], [False, None], self.case.get("description"))

    def test_mutually_exclusive_case_11(self):
        self.set_up(11)

        variation = self.vwo_instance.activate(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertEqual(variation, self.case.get("expectation"), self.case.get("description"))
        self.assertEqual(self.user_storage.get(self.user_id, self.campaign_key).get("campaignKey"), self.campaign_key)

        self.vwo_instance.config.settings_file.get("groups").get("1").get("campaigns").append(3)
        self.vwo_instance.config.settings_file.get("campaignGroups").update({"3": 1})

        variation = self.vwo_instance.activate(
            self.campaign_key,
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )
        self.assertEqual(variation, self.case.get("expectation"), self.case.get("description"))

    def test_mutually_exclusive_case_12(self):
        self.set_up(12)

        self.vwo_instance.activate(
            "c1",
            self.user_id,
            custom_variables=self.custom_variables,
            variation_targeting_variables=self.variation_targeting_variables,
        )

        self.assertEqual(self.user_storage.get(self.user_id, "c1").get("campaignKey"), "c1")

        self.assertEqual(
            self.vwo_instance.activate(
                self.campaign_key,
                self.user_id,
                custom_variables=self.custom_variables,
                variation_targeting_variables=self.variation_targeting_variables,
            ),
            self.case.get("expectation"),
            self.case.get("description"),
        )

    def test_mutually_exclusive_case_13(self):
        self.set_up(13)

        self.assertEqual(
            self.vwo_instance.activate(
                self.campaign_key,
                self.user_id,
                custom_variables=self.custom_variables,
                variation_targeting_variables=self.variation_targeting_variables,
            ),
            self.case.get("expectation"),
            self.case.get("description"),
        )
