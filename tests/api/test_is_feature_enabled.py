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
from ..data.settings_file_and_user_expectations import USER_EXPECTATIONS

from ..config.config import TEST_LOG_LEVEL

class ClientUserStorage:
    def __init__(self):
        self.storage = {}

    def get(self, user_id, campaign_key):
        return self.storage.get((user_id, campaign_key))

    def set(self, user_data):
        self.storage[(user_data.get("userId"), user_data.get("campaignKey"))] = user_data


class IsFeatureEnabledTest(unittest.TestCase):
    def set_up(self, config_variant="AB_T_50_W_50_50"):
        self.user_id = str(random.random())
        self.settings_file = json.dumps(SETTINGS_FILES.get(config_variant))

        self.vwo = vwo.launch(self.settings_file, is_development_mode=True, log_level=TEST_LOG_LEVEL)
        self.campaign_key = config_variant
        try:
            self.goal_identifier = SETTINGS_FILES[config_variant]["campaigns"][0]["goals"][0]["identifier"]
        except Exception:
            pass

    def test_is_feature_enabled_wrong_campaign_key_passed(self):
        self.set_up("FR_T_0_W_100")
        result = self.vwo.is_feature_enabled("not_a_campaign_key", "user")
        self.assertIs(result, False)

    def test_is_feature_enabled_wrong_campaign_type_passed(self):
        self.set_up("AB_T_50_W_50_50")
        result = self.vwo.is_feature_enabled("AB_T_50_W_50_50", "user")
        self.assertIs(result, False)

    def test_is_feature_enabled_wrong_parmas_passed(self):
        self.set_up("FR_T_0_W_100")
        self.assertIs(self.vwo.is_feature_enabled(123, 456), False)

    def test_is_feature_enabled_FR_W_0(self):
        self.set_up("FR_T_0_W_100")
        for test in USER_EXPECTATIONS.get("T_0_W_10_20_30_40"):
            self.assertIs(self.vwo.is_feature_enabled("FR_T_0_W_100", test["user"]), test["variation"] is not None)

    def test_is_feature_enabled_FR_W_25(self):
        self.set_up("FR_T_25_W_100")
        for test in USER_EXPECTATIONS.get("T_25_W_10_20_30_40"):
            self.assertIs(self.vwo.is_feature_enabled("FR_T_25_W_100", test["user"]), test["variation"] is not None)

    def test_is_feature_enabled_FR_W_50(self):
        self.set_up("FR_T_50_W_100")
        for test in USER_EXPECTATIONS.get("T_50_W_10_20_30_40"):
            self.assertIs(self.vwo.is_feature_enabled("FR_T_50_W_100", test["user"]), test["variation"] is not None)

    def test_is_feature_enabled_FR_W_75(self):
        self.set_up("FR_T_75_W_100")
        for test in USER_EXPECTATIONS.get("T_75_W_10_20_30_40"):
            self.assertIs(self.vwo.is_feature_enabled("FR_T_75_W_100", test["user"]), test["variation"] is not None)

    def test_is_feature_enabled_FR_W_100(self):
        self.set_up("FR_T_100_W_100")
        for test in USER_EXPECTATIONS.get("T_100_W_10_20_30_40"):
            self.assertIs(self.vwo.is_feature_enabled("FR_T_100_W_100", test["user"]), test["variation"] is not None)

    def test_is_feature_enabled_FT_T_75_W_10_20_30_40(self):
        self.set_up("FT_T_75_W_10_20_30_40")
        feature_not_enabled_variations = ["Control"]
        for test in USER_EXPECTATIONS["T_75_W_10_20_30_40"]:
            self.assertIs(
                self.vwo.is_feature_enabled("FT_T_75_W_10_20_30_40", test["user"]),
                test["variation"] is not None and test["variation"] not in feature_not_enabled_variations,
            )

    def test_is_feature_enabled_raises_exception(self):
        with mock.patch("vwo.helpers.validate_util.is_valid_string", side_effect=Exception("Test")):
            self.set_up()
            self.assertIs(False, self.vwo.is_feature_enabled("SOME_CAMPAIGN", "USER"))

    def test_is_feature_enabled_FT_T_75_W_10_20_30_40_WS_true(self):
        self.set_up("FT_T_75_W_10_20_30_40_WS")
        feature_not_enabled_variations = ["Control"]
        true_custom_variables = {"a": 987.1234, "hello": "world"}
        for test in USER_EXPECTATIONS["T_75_W_10_20_30_40"]:
            self.assertIs(
                self.vwo.is_feature_enabled(
                    "FT_T_75_W_10_20_30_40_WS", test["user"], custom_variables=true_custom_variables
                ),
                test["variation"] is not None and test["variation"] not in feature_not_enabled_variations,
            )

    def test_is_feature_enabled_FT_T_75_W_10_20_30_40_WS_false(self):
        self.set_up("FT_T_75_W_10_20_30_40_WS")
        false_custom_variables = {"a": 987.12, "hello": "world_world"}
        for test in USER_EXPECTATIONS["T_75_W_10_20_30_40"]:
            self.assertIs(
                self.vwo.is_feature_enabled(
                    "FT_T_75_W_10_20_30_40_WS", test["user"], custom_variables=false_custom_variables
                ),
                False,
            )

    def test_is_feature_enabled_FT_T_75_W_10_20_30_40_WS_false_custom_variables_in_kwargs(self):
        self.set_up("FT_T_75_W_10_20_30_40_WS")
        false_custom_variables = {"a": 987.12, "hello": "world_world"}
        for test in USER_EXPECTATIONS["T_75_W_10_20_30_40"]:
            self.assertIs(
                self.vwo.is_feature_enabled(
                    "FT_T_75_W_10_20_30_40_WS", test["user"], custom_variables=false_custom_variables
                ),
                False,
            )

    def test_is_feature_enabled_against_FT_100_W_33_33_33_WS_WW_False(self):
        vwo_client_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("FT_100_W_33_33_33_WS_WW")),
            log_level=TEST_LOG_LEVEL,
            is_development_mode=True,
        )
        false_variation_targeting_variables = {"chrome": "true", "safari": "false", "browser": "firefox 106.69"}
        false_custom_variables = {
            "contains_vwo": "legends say that vwo is the best",
            "regex_for_no_zeros": 1223123,
            "regex_for_all_letters": "dsfASF",
            "regex_for_small_letters": "sadfksjdf",
            "regex_real_number": 12321.2242,
            "regex_for_zeros": 0,
            "is_equal_to": "!equal_to_variable",
            "contains": "contains_variable",
            "regex_for_capital_letters": "SADFLSDLF",
            "is_not_equal_to": "is_not_equal_to_variable",
            "this_is_regex": "this    is    regex",
            "starts_with": "starts_with_variable",
        }
        for test in USER_EXPECTATIONS.get("AB_T_100_W_33_33_33"):
            self.assertIs(
                vwo_client_instance.is_feature_enabled(
                    "FT_100_W_33_33_33_WS_WW",
                    test["user"],
                    custom_variables=false_custom_variables,
                    variation_targeting_variables=false_variation_targeting_variables,
                ),  # noqa:501
                False,
            )

    def test_is_feature_enabled_against_FT_100_W_33_33_33_WS_WW(self):
        vwo_client_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("FT_100_W_33_33_33_WS_WW")),
            log_level=TEST_LOG_LEVEL,
            is_development_mode=True,
        )
        true_variation_targeting_variables = {"chrome": "false", "safari": "true", "browser": "chrome 107.107"}
        false_custom_variables = {
            "contains_vwo": "legends say that vwo is the best",
            "regex_for_no_zeros": 1223123,
            "regex_for_all_letters": "dsfASF",
            "regex_for_small_letters": "sadfksjdf",
            "regex_real_number": 12321.2242,
            "regex_for_zeros": 0,
            "is_equal_to": "!equal_to_variable",
            "contains": "contains_variable",
            "regex_for_capital_letters": "SADFLSDLF",
            "is_not_equal_to": "is_not_equal_to_variable",
            "this_is_regex": "this    is    regex",
            "starts_with": "starts_with_variable",
        }
        feature_not_enabled_variations = ["Control", "Variation-2"]
        for test in USER_EXPECTATIONS.get("AB_T_100_W_33_33_33"):
            self.assertEquals(
                vwo_client_instance.is_feature_enabled(
                    "FT_100_W_33_33_33_WS_WW",
                    test["user"],
                    custom_variables=false_custom_variables,
                    variation_targeting_variables=true_variation_targeting_variables,
                ),  # noqa:501
                test["variation"] is not None and test["variation"] not in feature_not_enabled_variations,
            )

    def test_is_feature_enabled_invalid_should_track_returning_user_value_passed(self):
        self.set_up("FT_T_100_W_10_20_30_40")
        result = []
        result.append(self.vwo.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user='test'))
        result.append(self.vwo.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user=100))
        result.append(self.vwo.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user=[]))
        result.append(self.vwo.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user=()))
        result.append(self.vwo.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user={}))
        self.assertListEqual(result, [False, False, False, False, False])

    def test_is_feature_enabled_valid_should_track_returning_user_value_passed(self):
        self.set_up("FT_T_100_W_10_20_30_40")
        result = self.vwo.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user=True)
        self.assertIs(result, True)

    def test_is_feature_enabled_check_dedup_no_user_storage_provided(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("FT_T_100_W_10_20_30_40")),
            is_development_mode=True,
            log_level=40,
            should_track_returning_user=True
        )

        with mock.patch("vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None) as mock_event_dispatcher_dispatch:
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 2)

            # Override global should_track_returning_user True value with False
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user=False)
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 3)
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user=False)
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 4)
            mock_event_dispatcher_dispatch.reset_mock()

    def test_is_feature_enabled_check_dedup_user_storage_provided(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("FT_T_100_W_10_20_30_40")),
            is_development_mode=True,
            log_level=40,
            should_track_returning_user=False,
            user_storage=ClientUserStorage()
        )

        with mock.patch("vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None) as mock_event_dispatcher_dispatch:
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)

            # Override global should_track_returning_user False value with True
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user=True)
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 2)
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user", should_track_returning_user=True)
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 3)
            mock_event_dispatcher_dispatch.reset_mock()

