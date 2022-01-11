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


class GetFeatureVariableValueTest(unittest.TestCase):
    def set_up(self, config_variant="AB_T_50_W_50_50"):
        self.user_id = str(random.random())
        self.settings_file = json.dumps(SETTINGS_FILES.get(config_variant))

        self.vwo = vwo.launch(self.settings_file, is_development_mode=True, log_level=TEST_LOG_LEVEL)
        self.campaign_key = config_variant
        try:
            self.goal_identifier = SETTINGS_FILES[config_variant]["campaigns"][0]["goals"][0]["identifier"]
        except Exception:
            pass

    # Test get_feature_variable_value from rollout
    def test_get_feature_variable_value_boolean_from_rollout(self):
        self.set_up("FR_T_75_W_100")
        BOOLEAN_VARIABLE = USER_EXPECTATIONS["ROLLOUT_VARIABLES"]["BOOLEAN_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_75_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FR_T_75_W_100", "BOOLEAN_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, BOOLEAN_VARIABLE)

    # Test get_feature_variable_value from rollout
    def test_get_feature_variable_value_type_string_from_rollout(self):
        self.set_up("FR_T_75_W_100")
        STRING_VARIABLE = USER_EXPECTATIONS["ROLLOUT_VARIABLES"]["STRING_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_75_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FR_T_75_W_100", "STRING_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, STRING_VARIABLE)

    # Test get_feature_variable_value from rollout
    def test_get_feature_variable_value_type_boolean_from_rollout(self):
        self.set_up("FR_T_75_W_100")
        DOUBLE_VARIABLE = USER_EXPECTATIONS["ROLLOUT_VARIABLES"]["DOUBLE_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_75_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FR_T_75_W_100", "DOUBLE_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, DOUBLE_VARIABLE)

    # Test get_feature_variable_value from rollout
    def test_get_feature_variable_value_type_integer_from_rollout(self):
        self.set_up("FR_T_75_W_100")
        INTEGER_VARIABLE = USER_EXPECTATIONS["ROLLOUT_VARIABLES"]["INTEGER_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_75_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FR_T_75_W_100", "INTEGER_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, INTEGER_VARIABLE)

    # Test get_feature_variable_value from rollout
    def test_get_feature_variable_value_type_json_from_rollout(self):
        self.set_up("FR_T_75_W_100")
        JSON_VARIABLE = USER_EXPECTATIONS["ROLLOUT_VARIABLES"]["JSON_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_75_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FR_T_75_W_100", "JSON_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, JSON_VARIABLE)

    # Test get_feature_variable_value from feature test from different feature splits
    def test_get_feature_variable_value_type_string_from_feature_test_t_0(self):
        self.set_up("FT_T_0_W_10_20_30_40")
        STRING_VARIABLE = USER_EXPECTATIONS["STRING_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_0_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FT_T_0_W_10_20_30_40", "STRING_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, STRING_VARIABLE[test["variation"]])

    def test_get_feature_variable_value_type_string_from_feature_test_t_25(self):
        self.set_up("FT_T_25_W_10_20_30_40")
        STRING_VARIABLE = USER_EXPECTATIONS["STRING_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_25_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FT_T_25_W_10_20_30_40", "STRING_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, STRING_VARIABLE[test["variation"]])

    def test_get_feature_variable_value_type_string_from_feature_test_t_50(self):
        self.set_up("FT_T_50_W_10_20_30_40")
        STRING_VARIABLE = USER_EXPECTATIONS["STRING_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_50_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FT_T_50_W_10_20_30_40", "STRING_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, STRING_VARIABLE[test["variation"]])

    def test_get_feature_variable_value_type_string_from_feature_test_t_75(self):
        self.set_up("FT_T_75_W_10_20_30_40")
        STRING_VARIABLE = USER_EXPECTATIONS["STRING_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_75_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FT_T_75_W_10_20_30_40", "STRING_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, STRING_VARIABLE[test["variation"]])

    def test_get_feature_variable_value_type_string_from_feature_test_t_100(self):
        self.set_up("FT_T_100_W_10_20_30_40")
        STRING_VARIABLE = USER_EXPECTATIONS["STRING_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_100_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FT_T_100_W_10_20_30_40", "STRING_VARIABLE", test["user"])
            if result:
                self.assertEquals(result, STRING_VARIABLE[test["variation"]])

    def test_get_feature_variable_value_type_string_from_feature_test_t_100_isFeatureEnabled(self):
        # isFeatureEnabled is False for variation-1 and variation-3,
        # should return variable from Control
        self.set_up("FT_T_100_W_10_20_30_40_IFEF")
        STRING_VARIABLE = USER_EXPECTATIONS["STRING_VARIABLE"]
        for test in USER_EXPECTATIONS.get("T_100_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value("FT_T_100_W_10_20_30_40_IFEF", "STRING_VARIABLE", test["user"])
            variation_name = test["variation"]
            if variation_name in ["Variation-1", "Variation-3"]:
                variation_name = "Control"
            if result:
                self.assertEquals(result, STRING_VARIABLE[variation_name])

    def test_get_feature_variable_wrong_variable_types(self):
        self.set_up("FR_WRONG_VARIABLE_TYPE")
        tests = [
            ("STRING_TO_INTEGER", 123, "integer", int),
            ("STRING_TO_FLOAT", 123.456, "double", float),
            ("BOOLEAN_TO_STRING", "True", "string", str),
            ("INTEGER_TO_STRING", "24", "string", str),
            ("INTEGER_TO_FLOAT", 24.0, "double", float),
            ("FLOAT_TO_STRING", "24.24", "string", str),
            ("FLOAT_TO_INTEGER", 24, "integer", int),
            ("JSON_STRING_TO_JSON", {"json": "json"}, "json", dict),
        ]
        for test in tests:
            result = self.vwo.get_feature_variable_value("FR_WRONG_VARIABLE_TYPE", test[0], "Zin")
            self.assertEquals(result, test[1])
            self.assertTrue(type(result) is test[3])

    # Testing private method _get_feature_variable

    def test_get_feature_variable_wrong_variable_types_return_none(self):
        self.set_up("FR_WRONG_VARIABLE_TYPE")
        tests = [
            ("WRONG_BOOLEAN", None, "boolean", None),
            ("WRONG_JSON_1", None, "json", None),
            ("WRONG_JSON_2", None, "json", None),
            ("WRONG_JSON_3", None, "json", None),
            ("WRONG_JSON_4", None, "json", None),
        ]
        for test in tests:
            result = self.vwo.get_feature_variable_value("FR_WRONG_VARIABLE_TYPE", test[0], "Zin")
            self.assertEquals(result, test[1])

    def test_get_feature_variable_invalid_params(self):
        self.set_up("FR_T_100_W_100")
        self.assertIsNone(self.vwo.get_feature_variable_value(123, 456, 789))

    def test_get_feature_variable_invalid_campaign_key(self):
        self.set_up("FR_T_100_W_100")
        self.assertIsNone(self.vwo.get_feature_variable_value("not_a_campaign", "STRING_VARIABLE", "Zin"))

    def test_get_feature_variable_invalid_campaign_type(self):
        self.set_up("AB_T_50_W_50_50")
        self.assertIsNone(self.vwo.get_feature_variable_value("AB_T_50_W_50_50", "STRING_VARIABLE", "Zin"))

    # test api raises exception
    # mock.patch referenced from https://stackoverflow.com/a/19107511
    def test_get_feature_variable_raises_exception(self):
        with mock.patch("vwo.helpers.validate_util.is_valid_string", side_effect=Exception("Test")):
            self.set_up()
            self.assertIs(None, self.vwo.get_feature_variable_value("SOME_CAMPAIGN", "VARIABLE_KEY", "USER_ID"))

    def test_get_feature_variable_value_type_string_from_feature_test_t_75_WS_true(self):
        self.set_up("FT_T_75_W_10_20_30_40_WS")
        STRING_VARIABLE = USER_EXPECTATIONS["STRING_VARIABLE"]
        true_custom_variables = {"a": 987.1234, "hello": "world"}
        for test in USER_EXPECTATIONS.get("T_75_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value(
                "FT_T_75_W_10_20_30_40_WS", "STRING_VARIABLE", test["user"], custom_variables=true_custom_variables
            )
            if result:
                self.assertEquals(result, STRING_VARIABLE[test["variation"]])

    def test_get_feature_variable_value_type_string_from_feature_test_t_75_WS_false(self):
        self.set_up("FT_T_75_W_10_20_30_40_WS")
        false_custom_variables = {"a": 987.12, "hello": "world_world"}
        for test in USER_EXPECTATIONS.get("T_75_W_10_20_30_40"):
            result = self.vwo.get_feature_variable_value(
                "FT_T_75_W_10_20_30_40_WS", "STRING_VARIABLE", test["user"], custom_variables=false_custom_variables
            )
            self.assertEquals(result, None)

    def test_get_feature_variable_value_against_FT_100_W_33_33_33_WS_WW_False(self):
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
                vwo_client_instance.get_feature_variable_value(
                    "FT_100_W_33_33_33_WS_WW",
                    "STRING_VARIABLE",
                    test["user"],
                    custom_variables=false_custom_variables,
                    variation_targeting_variables=false_variation_targeting_variables,
                ),  # noqa:501
                None,
            )

    def test_get_feature_variable_value_string_against_FT_100_W_33_33_33_WS_WW(self):
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
        variables = {
            "Control": {
                "STRING_VARIABLE": "CONTROL_STRING_VARIABLE",
                "INTEGER_VARIABLE": 0,
                "FLOAT_VARIABLE": 0,
                "JSON_VARIABLE": {"data": "CONTROL_JSON_VARIABLE"},
            },
            "Variation-1": {
                "STRING_VARIABLE": "VARIATION-1_STRING_VARIABLE",
                "INTEGER_VARIABLE": 1,
                "FLOAT_VARIABLE": 1.1,
                "JSON_VARIABLE": {"data": "VARIATION-1_JSON_VARIABLE"},
            },
            "Variation-2": {
                "STRING_VARIABLE": "VARIATION-2_STRING_VARIABLE",
                "INTEGER_VARIABLE": 2,
                "FLOAT_VARIABLE": 2.2,
                "JSON_VARIABLE": {"data": "VARIATION-2_JSON_VARIABLE"},
            },
        }
        feature_not_enabled_variations = ["Control", "Variation-2"]
        for test in USER_EXPECTATIONS.get("AB_T_100_W_33_33_33"):
            result = vwo_client_instance.get_feature_variable_value(
                "FT_100_W_33_33_33_WS_WW",
                "STRING_VARIABLE",
                test["user"],
                custom_variables=false_custom_variables,
                variation_targeting_variables=true_variation_targeting_variables,
            )  # noqa:501
            if test["variation"] not in feature_not_enabled_variations:
                expectation = variables.get(test["variation"]).get("STRING_VARIABLE")
            else:
                expectation = variables.get("Control").get("STRING_VARIABLE")
            self.assertEquals(result, expectation)

    def test_get_feature_variable_value_integer_against_FT_100_W_33_33_33_WS_WW(self):
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
        variables = {
            "Control": {
                "STRING_VARIABLE": "CONTROL_STRING_VARIABLE",
                "INTEGER_VARIABLE": 0,
                "FLOAT_VARIABLE": 0,
                "JSON_VARIABLE": {"data": "CONTROL_JSON_VARIABLE"},
            },
            "Variation-1": {
                "STRING_VARIABLE": "VARIATION-1_STRING_VARIABLE",
                "INTEGER_VARIABLE": 1,
                "FLOAT_VARIABLE": 1.1,
                "JSON_VARIABLE": {"data": "VARIATION-1_JSON_VARIABLE"},
            },
            "Variation-2": {
                "STRING_VARIABLE": "VARIATION-2_STRING_VARIABLE",
                "INTEGER_VARIABLE": 2,
                "FLOAT_VARIABLE": 2.2,
                "JSON_VARIABLE": {"data": "VARIATION-2_JSON_VARIABLE"},
            },
        }
        feature_not_enabled_variations = ["Control", "Variation-2"]
        for test in USER_EXPECTATIONS.get("AB_T_100_W_33_33_33"):
            result = vwo_client_instance.get_feature_variable_value(
                "FT_100_W_33_33_33_WS_WW",
                "INTEGER_VARIABLE",
                test["user"],
                custom_variables=false_custom_variables,
                variation_targeting_variables=true_variation_targeting_variables,
            )  # noqa:501
            if test["variation"] not in feature_not_enabled_variations:
                expectation = variables.get(test["variation"]).get("INTEGER_VARIABLE")
            else:
                expectation = variables.get("Control").get("INTEGER_VARIABLE")
            self.assertEquals(result, expectation)

    def test_get_feature_variable_value_float_against_FT_100_W_33_33_33_WS_WW(self):
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
        variables = {
            "Control": {
                "STRING_VARIABLE": "CONTROL_STRING_VARIABLE",
                "INTEGER_VARIABLE": 0,
                "FLOAT_VARIABLE": 0,
                "JSON_VARIABLE": {"data": "CONTROL_JSON_VARIABLE"},
            },
            "Variation-1": {
                "STRING_VARIABLE": "VARIATION-1_STRING_VARIABLE",
                "INTEGER_VARIABLE": 1,
                "FLOAT_VARIABLE": 1.1,
                "JSON_VARIABLE": {"data": "VARIATION-1_JSON_VARIABLE"},
            },
            "Variation-2": {
                "STRING_VARIABLE": "VARIATION-2_STRING_VARIABLE",
                "INTEGER_VARIABLE": 2,
                "FLOAT_VARIABLE": 2.2,
                "JSON_VARIABLE": {"data": "VARIATION-2_JSON_VARIABLE"},
            },
        }
        feature_not_enabled_variations = ["Control", "Variation-2"]
        for test in USER_EXPECTATIONS.get("AB_T_100_W_33_33_33"):
            result = vwo_client_instance.get_feature_variable_value(
                "FT_100_W_33_33_33_WS_WW",
                "FLOAT_VARIABLE",
                test["user"],
                custom_variables=false_custom_variables,
                variation_targeting_variables=true_variation_targeting_variables,
            )  # noqa:501
            if test["variation"] not in feature_not_enabled_variations:
                expectation = variables.get(test["variation"]).get("FLOAT_VARIABLE")
            else:
                expectation = variables.get("Control").get("FLOAT_VARIABLE")
            self.assertEquals(result, expectation)

    def test_get_feature_variable_value_json_against_FT_100_W_33_33_33_WS_WW(self):
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
        variables = {
            "Control": {
                "STRING_VARIABLE": "CONTROL_STRING_VARIABLE",
                "INTEGER_VARIABLE": 0,
                "FLOAT_VARIABLE": 0,
                "JSON_VARIABLE": {"data": "CONTROL_JSON_VARIABLE"},
            },
            "Variation-1": {
                "STRING_VARIABLE": "VARIATION-1_STRING_VARIABLE",
                "INTEGER_VARIABLE": 1,
                "FLOAT_VARIABLE": 1.1,
                "JSON_VARIABLE": {"data": "VARIATION-1_JSON_VARIABLE"},
            },
            "Variation-2": {
                "STRING_VARIABLE": "VARIATION-2_STRING_VARIABLE",
                "INTEGER_VARIABLE": 2,
                "FLOAT_VARIABLE": 2.2,
                "JSON_VARIABLE": {"data": "VARIATION-2_JSON_VARIABLE"},
            },
        }
        feature_not_enabled_variations = ["Control", "Variation-2"]
        for test in USER_EXPECTATIONS.get("AB_T_100_W_33_33_33"):
            result = vwo_client_instance.get_feature_variable_value(
                "FT_100_W_33_33_33_WS_WW",
                "JSON_VARIABLE",
                test["user"],
                custom_variables=false_custom_variables,
                variation_targeting_variables=true_variation_targeting_variables,
            )  # noqa:501
            if test["variation"] not in feature_not_enabled_variations:
                expectation = variables.get(test["variation"]).get("JSON_VARIABLE")
            else:
                expectation = variables.get("Control").get("JSON_VARIABLE")
            self.assertEquals(result, expectation)

    def test_get_feature_variable_value_fail_prior_campaign_activation_for_feature_rollout_campaign(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("FR_T_75_W_100")),
            is_development_mode=True,
            log_level=TEST_LOG_LEVEL,
            should_track_returning_user=False,
            user_storage=ClientUserStorage(),
        )

        result = vwo_instance.get_feature_variable_value("FR_T_75_W_100", "FLOAT_VARIABLE", "Ashley")
        self.assertIsNone(result)

    def test_get_feature_variable_value_pass_after_campaign_activation_for_feature_rollout_campaign(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("FR_T_75_W_100")),
            is_development_mode=True,
            log_level=TEST_LOG_LEVEL,
            should_track_returning_user=False,
            user_storage=ClientUserStorage(),
        )

        FLOAT_VARIABLE = USER_EXPECTATIONS["ROLLOUT_VARIABLES"]["DOUBLE_VARIABLE"]
        vwo_instance.is_feature_enabled("FR_T_75_W_100", "Ashley")
        result = vwo_instance.get_feature_variable_value("FR_T_75_W_100", "FLOAT_VARIABLE", "Ashley")
        self.assertEquals(result, FLOAT_VARIABLE)

    def test_get_feature_variable_value_when_opted_out(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("FT_T_100_W_10_20_30_40")), is_development_mode=True, log_level=40
        )

        result = vwo_instance.get_feature_variable_value("FT_T_100_W_10_20_30_40", "STRING_VARIABLE", "user")
        self.assertEqual(result, "Variation-3 string")

        api_response = vwo_instance.set_opt_out()
        self.assertIs(api_response, True)

        result = vwo_instance.get_feature_variable_value("FT_T_100_W_10_20_30_40", "STRING_VARIABLE", "user")
        self.assertIs(result, None)
