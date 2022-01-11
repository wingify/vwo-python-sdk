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


class TrackTest(unittest.TestCase):
    def set_up(self, config_variant="AB_T_50_W_50_50", **kwargs):
        self.user_id = str(random.random())
        self.settings_file = json.dumps(SETTINGS_FILES.get(config_variant))

        self.vwo = vwo.launch(
            self.settings_file,
            is_development_mode=True,
            log_level=TEST_LOG_LEVEL,
            user_storage=kwargs.get("user_storage"),
        )
        self.campaign_key = config_variant
        try:
            self.goal_identifier = SETTINGS_FILES[config_variant]["campaigns"][0]["goals"][0]["identifier"]
        except Exception:
            pass

    def test_track_invalid_params(self):
        self.set_up()
        self.assertIs(self.vwo.track(123, 456, 789), None)

    def test_track_with_no_campaign_key_found(self):
        self.set_up("AB_T_50_W_50_50")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track("NO_SUCH_CAMPAIGN_KEY", test["user"], self.goal_identifier), None)

    def test_track_with_no_goal_identifier_found(self):
        self.set_up("AB_T_50_W_50_50")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test["user"], "NO_SUCH_GOAL_IDENTIFIER"), None)

    def test_track_wrong_campaign_type_passed(self):
        self.set_up("FR_T_0_W_100")
        result = self.vwo.track("FR_T_0_W_100", "user", "CUSTOM")
        self.track_test(result, False)

    def test_track_against_campaign_traffic_50_and_split_50_50(self):
        self.set_up("AB_T_50_W_50_50")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(
                self.vwo.track(self.campaign_key, test["user"], self.goal_identifier), test["variation"] is not None
            )

    def test_track_against_campaign_traffic_100_and_split_50_50_r_int(self):
        # It's goal_type is revenue, so test revenue
        self.set_up("AB_T_100_W_50_50")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(
                self.vwo.track(self.campaign_key, test["user"], self.goal_identifier, revenue_value=23),
                test["variation"] is not None,
            )

    def test_track_with_event_arch_and_event_batching_disabled(self):
        self.set_up("AB_T_100_W_50_50")
        event_arch_settings_file = SETTINGS_FILES.get("AB_T_100_W_50_50").copy()
        event_arch_settings_file["isEventArchEnabled"] = True
        self.vwo = vwo.launch(json.dumps(event_arch_settings_file), is_development_mode=True, log_level=TEST_LOG_LEVEL)

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch_events", return_value=None
        ) as mock_event_dispatcher_dispatch:
            self.vwo.event_dispatcher.dispatch = mock.MagicMock()
            self.vwo.track(self.campaign_key, "Ashley", self.goal_identifier, revenue_value=23)
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)
            self.vwo.track(self.campaign_key, "Ashley", self.goal_identifier, revenue_value=23)
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 2)
            mock_event_dispatcher_dispatch.reset_mock()
            self.vwo.event_dispatcher.dispatch.assert_not_called()

    def test_track_with_event_arch_and_event_batching_enabled(self):
        self.set_up("AB_T_100_W_50_50")
        event_arch_settings_file = SETTINGS_FILES.get("AB_T_100_W_50_50").copy()
        event_arch_settings_file["isEventArchEnabled"] = True
        self.vwo = vwo.launch(
            json.dumps(event_arch_settings_file),
            is_development_mode=True,
            log_level=TEST_LOG_LEVEL,
            batch_events={"events_per_request": 5, "request_time_interval": 1},
        )

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            self.vwo.event_dispatcher.dispatch_events = mock.MagicMock()
            self.vwo.track(self.campaign_key, "Ashley", self.goal_identifier, revenue_value=23)
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)
            self.vwo.track(self.campaign_key, "Ashley", self.goal_identifier, revenue_value=23)
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 2)
            mock_event_dispatcher_dispatch.reset_mock()
            self.vwo.event_dispatcher.dispatch_events.assert_not_called()

    def test_track_against_campaign_traffic_100_and_split_50_50_r_float(self):
        # It's goal_type is revenue, so test revenue
        self.set_up("AB_T_100_W_50_50")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(
                self.vwo.track(self.campaign_key, test["user"], self.goal_identifier, revenue_value=23.3),
                test["variation"] is not None,
            )

    def test_track_against_campaign_traffic_100_and_split_50_50_r_str(self):
        # It's goal_type is revenue, so test revenue
        self.set_up("AB_T_100_W_50_50")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(
                self.vwo.track(self.campaign_key, test["user"], self.goal_identifier, revenue_value="23.3"),
                test["variation"] is not None,
            )

    def test_track_against_campaign_traffic_100_and_split_50_50_no_r(self):
        # It's goal_type is revenue, so test revenue
        self.set_up("AB_T_100_W_50_50")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(self.vwo.track(self.campaign_key, test["user"], self.goal_identifier), False)

    def test_track_against_campaign_traffic_100_and_split_50_50_kwargs(self):
        # It's goal_type is revenue, so test revenue
        self.set_up("AB_T_100_W_50_50")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(
                self.vwo.track(self.campaign_key, test["user"], self.goal_identifier, revenue_value=23),
                test["variation"] is not None,
            )

    def test_track_against_campaign_traffic_100_and_split_20_80(self):
        self.set_up("AB_T_100_W_20_80")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(
                self.vwo.track(self.campaign_key, test["user"], self.goal_identifier), test["variation"] is not None
            )

    def test_track_against_campaign_traffic_20_and_split_10_90(self):
        self.set_up("AB_T_20_W_10_90")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(
                self.vwo.track(self.campaign_key, test["user"], self.goal_identifier), test["variation"] is not None
            )

    def test_track_against_campaign_traffic_100_and_split_0_100(self):
        self.set_up("AB_T_100_W_0_100")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(
                self.vwo.track(self.campaign_key, test["user"], self.goal_identifier), test["variation"] is not None
            )

    def test_track_against_campaign_traffic_100_and_split_33_x3(self):
        self.set_up("AB_T_100_W_33_33_33")
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.track_test(
                self.vwo.track(self.campaign_key, test["user"], self.goal_identifier), test["variation"] is not None
            )

    # test api raises exception
    # mock.patch referenced from https://stackoverflow.com/a/19107511
    def test_track_raises_exception(self):
        with mock.patch("vwo.helpers.validate_util.is_valid_string", side_effect=Exception("Test")):
            self.set_up()
            self.assertIs(False, self.vwo.track("SOME_CAMPAIGN", "USER", "GOAL"))

    def test_track_with_with_no_custom_variables_fails(self):
        self.set_up("T_100_W_50_50_WS")
        for test in USER_EXPECTATIONS["AB_T_100_W_50_50"]:
            self.track_test(self.vwo.track("T_100_W_50_50_WS", test["user"], "ddd"), False)

    def test_track_revenue_value_and_custom_variables_passed_in_kwargs(self):
        def mock_track(campaign_key, user_id, goal_identifier, **kwargs):
            revenue_value = kwargs.get("revenue_value")
            custom_variables = kwargs.get("custom_variables")
            return {
                "campaign_key": campaign_key,
                "user_id": user_id,
                "goal_identifier": goal_identifier,
                "revenue_value": revenue_value,
                "custom_variables": custom_variables,
            }

        arguments_to_track = {
            "campaign_key": "TEST_TRACK",
            "user_id": "user_id",
            "goal_identifier": "GOAL_ID",
            "revenue_value": 100,
            "custom_variables": {"a": "b"},
        }
        self.assertDictEqual(
            mock_track(
                arguments_to_track.get("campaign_key"),
                arguments_to_track.get("user_id"),
                arguments_to_track.get("goal_identifier"),
                revenue_value=arguments_to_track.get("revenue_value"),
                custom_variables=arguments_to_track.get("custom_variables"),
            ),
            arguments_to_track,
        )

    def test_track_with_presegmentation_true(self):
        self.set_up("T_50_W_50_50_WS")
        true_custom_variables = {"a": 987.1234, "hello": "world"}
        for test in USER_EXPECTATIONS["AB_T_50_W_50_50"]:
            self.track_test(
                self.vwo.track("T_50_W_50_50_WS", test["user"], "ddd", custom_variables=true_custom_variables),
                test["variation"] is not None,
            )

    def test_track_with_presegmentation_false(self):
        self.set_up("T_50_W_50_50_WS")
        false_custom_variables = {"a": 987.12, "hello": "world_world"}
        for test in USER_EXPECTATIONS["AB_T_50_W_50_50"]:
            self.track_test(
                self.vwo.track("T_50_W_50_50_WS", test["user"], "ddd", custom_variables=false_custom_variables), False
            )

    def test_track_with_no_dsl_remains_unaffected(self):
        self.set_up("AB_T_50_W_50_50")
        true_custom_variables = {"a": 987.1234, "hello": "world"}
        for test in USER_EXPECTATIONS["AB_T_50_W_50_50"]:
            self.track_test(
                self.vwo.track("AB_T_50_W_50_50", test["user"], "CUSTOM", custom_variables=true_custom_variables),
                test["variation"] is not None,
            )

    def test_track_with_no_custom_variables_fails(self):
        self.set_up("T_50_W_50_50_WS")
        for test in USER_EXPECTATIONS["AB_T_50_W_50_50"]:
            self.track_test(self.vwo.track("T_50_W_50_50_WS", test["user"], "ddd"), False)

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

    def test_track_against_T_100_W_33_33_33_WS_WW_None(self):
        self.set_up("T_100_W_33_33_33_WS_WW")
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
            self.track_test(
                self.vwo.track(
                    "T_100_W_33_33_33_WS_WW",
                    test["user"],
                    "CUSTOM",
                    custom_variables=false_custom_variables,
                    variation_targeting_variables=false_variation_targeting_variables,
                ),
                False,
            )

    def test_track_against_T_100_W_33_33_33_WS_WW(self):
        self.set_up("T_100_W_33_33_33_WS_WW")
        true_variation_targeting_variables = {"chrome": "false", "safari": "true", "browser": "chrome 107.107"}
        true_custom_variables = {
            "contains_vwo": "legends say that vwo is the best",
            "regex_for_no_zeros": 1223123,
            "regex_for_all_letters": "dsfASF",
            "regex_for_small_letters": "sadfksjdf",
            "regex_real_number": 12321.2242,
            "regex_for_zeros": 0,
            "is_equal_to": "equal_to_variable",
            "contains": "contains_variable",
            "regex_for_capital_letters": "SADFLSDLF",
            "is_not_equal_to": "is_not_equal_to_variable",
            "this_is_regex": "this    is    regex",
            "starts_with": "starts_with_variable",
        }
        for test in USER_EXPECTATIONS.get("AB_T_100_W_33_33_33"):
            self.track_test(
                self.vwo.track(
                    "T_100_W_33_33_33_WS_WW",
                    test["user"],
                    "CUSTOM",
                    custom_variables=true_custom_variables,
                    variation_targeting_variables=true_variation_targeting_variables,
                ),
                test["variation"] is not None,
            )

    def track_test(self, expected, actual):
        self.assertDictEqual(expected, {self.campaign_key: actual})

    def test_multi_track_none(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track1")
        expected = {"global_test_1": True, "feature_test_1": True}
        self.assertDictEqual(result, expected)

    def test_multi_track_list(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(["feature_test_1", "global_test_1"], "user", "track1")
        expected = {"global_test_1": True, "feature_test_1": True}
        self.assertDictEqual(result, expected)

    def test_multi_track_list_no_goal_found_should_return_false_in_map(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(["global_test_1", "feature_test_1"], "user", "track5")
        expected = {"global_test_1": False, "feature_test_1": False}
        self.assertDictEqual(result, expected)

    def test_single_track_in_list_no_goal_found_should_return_false_in_map(self,):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
        )
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(["feature_test_1"], "user", "track5")
        expected = {"feature_test_1": False}
        self.assertDictEqual(result, expected)

    def test_single_track_in_str_no_goal_found_should_return_None(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
        )
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track("feature_test_1", "user", "track5")
        expected = None
        self.assertEquals(result, expected)

    def test_multi_track_list_no_campaign_found_should_return_empty_map(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
        )
        vwo_instance.activate("feature_test_2", "user")
        result = vwo_instance.track(["feature_test_2"], "user", "track1")
        expected = {}
        self.assertDictEqual(result, expected)

    def test_multi_track_list_1_item_no_goal_found(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
        )
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(["feature_test_1"], "user", "track5")
        expected = {"feature_test_1": False}
        self.assertDictEqual(result, expected)

    # Preference type tests
    def test_all_goal_type_should_be_tracked_by_default_no_where_type_specified(self,):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2", revenue_value=1)
        expected = {"feature_test_1": True, "global_test_1": True}
        self.assertDictEqual(result, expected)

    def test_all_custom_should_be_tracked_specified_in_launch_api(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
            goal_type_to_track=vwo.GOAL_TYPES.CUSTOM,
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2")
        expected = {"global_test_1": True, "feature_test_1": False}
        self.assertDictEqual(result, expected)

    def test_all_revenue_should_be_tracked_specified_in_launch_api(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
            goal_type_to_track=vwo.GOAL_TYPES.REVENUE,
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2", revenue_value=10)
        expected = {"global_test_1": False, "feature_test_1": True}
        self.assertDictEqual(result, expected)

    def test_change_goal_type_preference_from_revenue_to_all(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
            goal_type_to_track=vwo.GOAL_TYPES.REVENUE,
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2", revenue_value=10, goal_type_to_track=vwo.GOAL_TYPES.ALL)
        expected = {"global_test_1": True, "feature_test_1": True}
        self.assertDictEqual(result, expected)

    def test_change_goal_type_preference_from_revenue_to_custom(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
            goal_type_to_track=vwo.GOAL_TYPES.REVENUE,
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2", revenue_value=10, goal_type_to_track=vwo.GOAL_TYPES.CUSTOM)
        expected = {"global_test_1": True, "feature_test_1": False}
        self.assertDictEqual(result, expected)

    def test_change_goal_type_preference_from_custom_to_all(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
            goal_type_to_track=vwo.GOAL_TYPES.CUSTOM,
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2", revenue_value=10, goal_type_to_track=vwo.GOAL_TYPES.ALL)
        expected = {"global_test_1": True, "feature_test_1": True}
        self.assertDictEqual(result, expected)

    def test_change_goal_type_preference_from_custom_to_revenue(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
            goal_type_to_track=vwo.GOAL_TYPES.CUSTOM,
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2", revenue_value=10, goal_type_to_track=vwo.GOAL_TYPES.REVENUE)
        expected = {"global_test_1": False, "feature_test_1": True}
        self.assertDictEqual(result, expected)

    def test_change_goal_type_preference_from_all_to_revenue(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
            goal_type_to_track=vwo.GOAL_TYPES.ALL,
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2", revenue_value=10, goal_type_to_track=vwo.GOAL_TYPES.REVENUE)
        expected = {"global_test_1": False, "feature_test_1": True}
        self.assertDictEqual(result, expected)

    def test_change_goal_type_preference_from_all_to_custom(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
            goal_type_to_track=vwo.GOAL_TYPES.ALL,
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2", goal_type_to_track=vwo.GOAL_TYPES.CUSTOM)
        expected = {"global_test_1": True, "feature_test_1": False}
        self.assertDictEqual(result, expected)

    def test_all_revenue_should_be_tracked_overwrite_specified_in_launch_api_1_should_fail_no_revenue(self,):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")),
            is_development_mode=True,
            log_level=40,
            user_storage=ClientUserStorage(),
            goal_type_to_track=vwo.GOAL_TYPES.REVENUE,
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.activate("feature_test_1", "user2")
        result = vwo_instance.track(None, "user", "track2", goal_type_to_track=vwo.GOAL_TYPES.ALL)
        expected = {"global_test_1": True, "feature_test_1": False}
        self.assertDictEqual(result, expected)

    def test_invalid_goal_type_passed_should_return_None(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")), is_development_mode=True
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "track2", goal_type_to_track="vwo.GOAL_TYPES.CUSTOM")
        self.assertIsNone(result)

    def test_no_global_goal_found(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")), is_development_mode=True
        )
        vwo_instance.activate("global_test_1", "user")
        vwo_instance.is_feature_enabled("feature_test_1", "user")
        result = vwo_instance.track(None, "user", "goal_not_existing")
        self.assertIsNone(result)

    def test_track_invalid_campaign_specifier_passed(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("GLOBAL_TRACK_SETTINGS_FILE")), is_development_mode=True
        )
        result = vwo_instance.track(True, "user", "goal_not_existing")
        self.assertIsNone(result)

    def test_track_should_add_goalIdentifiers_if_variation_is_found_in_user_storage_prior_track(self):
        user_storage = ClientUserStorage()
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("AB_T_100_W_50_50")), is_development_mode=True, user_storage=user_storage
        )
        vwo_instance.activate("AB_T_100_W_50_50", "user")
        vwo_instance.track("AB_T_100_W_50_50", "user", "CUSTOM")
        self.assertEquals(user_storage.get("user", "AB_T_100_W_50_50").get("goalIdentifiers"), "CUSTOM")

    def test_track_should_work_when_called_before_is_feature_enabled_when_no_user_storage_provided(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("FT_T_100_W_10_20_30_40")), is_development_mode=True)

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            vwo_instance.track("FT_T_100_W_10_20_30_40", "user", "FEATURE_TEST_GOAL")
            self.assertEqual(mock_event_dispatcher_dispatch.call_count, 1)
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user")
            self.assertEqual(mock_event_dispatcher_dispatch.call_count, 2)
            mock_event_dispatcher_dispatch.reset_mock()

    def test_track_should_work_when_called_before_activate_when_no_user_storage_provided(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_100_W_50_50")), is_development_mode=True)

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            vwo_instance.track("AB_T_100_W_50_50", "user", "CUSTOM")
            self.assertEqual(mock_event_dispatcher_dispatch.call_count, 1)
            vwo_instance.activate("AB_T_100_W_50_50", "user")
            self.assertEqual(mock_event_dispatcher_dispatch.call_count, 2)
            mock_event_dispatcher_dispatch.reset_mock()

    def test_track_should_fail_when_called_before_is_feature_enabled_when_user_storage_provided(self):
        user_storage = ClientUserStorage()
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("FT_T_100_W_10_20_30_40")),
            is_development_mode=True,
            user_storage=user_storage,
        )

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            vwo_instance.track("FT_T_100_W_10_20_30_40", "user", "FEATURE_TEST_GOAL")
            self.assertEqual(mock_event_dispatcher_dispatch.call_count, 0)
            vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user")
            self.assertEqual(mock_event_dispatcher_dispatch.call_count, 1)
            mock_event_dispatcher_dispatch.reset_mock()

    def test_track_should_fail_when_called_before_activate_when_user_storage_provided(self):
        user_storage = ClientUserStorage()
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("AB_T_100_W_50_50")), is_development_mode=True, user_storage=user_storage
        )

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            vwo_instance.track("AB_T_100_W_50_50", "user", "CUSTOM")
            self.assertEqual(mock_event_dispatcher_dispatch.call_count, 0)
            vwo_instance.activate("AB_T_100_W_50_50", "user")
            self.assertEqual(mock_event_dispatcher_dispatch.call_count, 1)
            mock_event_dispatcher_dispatch.reset_mock()

    def test_track_when_opted_out(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("AB_T_100_W_50_50")), is_development_mode=True, log_level=40
        )

        result = vwo_instance.track("AB_T_100_W_50_50", "user", "CUSTOM")
        self.assertEqual(result, {u"AB_T_100_W_50_50": True})
        api_response = vwo_instance.set_opt_out()
        self.assertIs(api_response, True)

        result = vwo_instance.track("AB_T_100_W_50_50", "user", "CUSTOM")
        self.assertIs(result, None)
