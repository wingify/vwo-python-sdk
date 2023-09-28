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

""" Various settings_file for testings

    Notes:
    Abbreviations: T = percentTraffic
                   W = weight split
                   AB = VISUAL_AB
                   FT = FEATURE_TEST
                   FR = FEATURE_ROLLOUT
                   IFEF = isFeatureEnabled is False
                   WS = With Segments
                   WW = With Whitelisting

    Campaigns key of each campaign is same as setttings_file name.
"""

SETTINGS_FILES = {
    "EMPTY_SETTINGS_FILE": {},
    "AB_T_50_W_50_50": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 230,
                "name": "Campaign-230",
                "percentTraffic": 50,
                "key": "AB_T_50_W_50_50",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "AB_T_100_W_50_50": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [
                    {"identifier": "abcd", "id": 1, "type": "REVENUE_TRACKING"},
                    {"identifier": "CUSTOM", "id": 214, "type": "CUSTOM_GOAL"},
                ],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "name": "Campaign-231",
                "percentTraffic": 100,
                "key": "AB_T_100_W_50_50",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "AB_T_100_W_20_80": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 215, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 20},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 80},
                ],
                "id": 232,
                "name": "Campaign-232",
                "percentTraffic": 100,
                "key": "AB_T_100_W_20_80",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "AB_T_20_W_10_90": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 216, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 10},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 90},
                ],
                "id": 233,
                "name": "Campaign-233",
                "percentTraffic": 20,
                "key": "AB_T_20_W_10_90",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "AB_T_100_W_0_100": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 217, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 0},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 100},
                ],
                "id": 234,
                "name": "Campaign-234",
                "percentTraffic": 100,
                "key": "AB_T_100_W_0_100",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "AB_T_100_W_33_33_33": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 218, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 33.3333},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 33.3333},
                    {"id": 3, "name": "Variation-2", "changes": {}, "weight": 33.3333},
                ],
                "id": 235,
                "name": "Campaign-235",
                "percentTraffic": 100,
                "key": "AB_T_100_W_33_33_33",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "DUMMY_SETTINGS_FILE": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "GOAL_NEW", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": "1", "name": "Control", "weight": 40},
                    {"id": "2", "name": "Variation-1", "weight": 60},
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 50,
                "key": "DUMMY_SETTINGS_FILE",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "FR_T_0_W_100": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [{"id": "1", "name": "Control", "weight": 100}],
                "variables": [
                    {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "this_is_a_string"},
                    {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                    {"id": 3, "key": "FLOAT_VARIABLE", "type": "double", "value": 123.456},
                    {"id": 4, "key": "BOOLEAN_VARIABLE", "type": "boolean", "value": True},
                    {
                        "id": 5,
                        "key": "JSON_VARIABLE",
                        "type": "json",
                        "value": {
                            "data_string": "this_is_a_string",
                            "data_integer": "123",
                            "data_boolean": True,
                            "data_double": 123.456,
                            "data_json": {"json": "json"},
                        },
                    },
                ],
                "id": 29,
                "name": "Campaign-29",
                "percentTraffic": 0,
                "key": "FR_T_0_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FR_T_25_W_100": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [],
                "variations": [{"id": "1", "name": "Control", "weight": 100}],
                "variables": [
                    {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "this_is_a_string"},
                    {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                    {"id": 3, "key": "FLOAT_VARIABLE", "type": "double", "value": 123.456},
                    {"id": 4, "key": "BOOLEAN_VARIABLE", "type": "boolean", "value": True},
                    {
                        "id": 5,
                        "key": "JSON_VARIABLE",
                        "type": "json",
                        "value": {
                            "data_string": "this_is_a_string",
                            "data_integer": "123",
                            "data_boolean": True,
                            "data_double": 123.456,
                            "data_json": {"json": "json"},
                        },
                    },
                ],
                "id": 29,
                "name": "Campaign-29",
                "percentTraffic": 25,
                "key": "FR_T_25_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FR_T_50_W_100": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [],
                "variations": [{"id": "1", "name": "Control", "weight": 100}],
                "variables": [
                    {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "this_is_a_string"},
                    {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                    {"id": 3, "key": "FLOAT_VARIABLE", "type": "double", "value": 123.456},
                    {"id": 4, "key": "BOOLEAN_VARIABLE", "type": "boolean", "value": True},
                    {
                        "id": 5,
                        "key": "JSON_VARIABLE",
                        "type": "json",
                        "value": {
                            "data_string": "this_is_a_string",
                            "data_integer": "123",
                            "data_boolean": True,
                            "data_double": 123.456,
                            "data_json": {"json": "json"},
                        },
                    },
                ],
                "id": 29,
                "name": "Campaign-29",
                "percentTraffic": 50,
                "key": "FR_T_50_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FR_T_75_W_100": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [],
                "variations": [{"id": "1", "name": "Control", "weight": 100}],
                "variables": [
                    {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "this_is_a_string"},
                    {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                    {"id": 3, "key": "FLOAT_VARIABLE", "type": "double", "value": 123.456},
                    {"id": 4, "key": "BOOLEAN_VARIABLE", "type": "boolean", "value": True},
                    {
                        "id": 5,
                        "key": "JSON_VARIABLE",
                        "type": "json",
                        "value": {
                            "data_string": "this_is_a_string",
                            "data_integer": "123",
                            "data_boolean": True,
                            "data_double": 123.456,
                            "data_json": {"json": "json"},
                        },
                    },
                ],
                "id": 29,
                "name": "Campaign-29",
                "percentTraffic": 75,
                "key": "FR_T_75_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FR_T_100_W_100": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [],
                "variations": [{"id": "1", "name": "Control", "weight": 100}],
                "variables": [
                    {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "this_is_a_string"},
                    {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                    {"id": 3, "key": "FLOAT_VARIABLE", "type": "double", "value": 123.456},
                    {"id": 4, "key": "BOOLEAN_VARIABLE", "type": "boolean", "value": True},
                    {
                        "id": 5,
                        "key": "JSON_VARIABLE",
                        "type": "json",
                        "value": {
                            "data_string": "this_is_a_string",
                            "data_integer": "123",
                            "data_boolean": True,
                            "data_double": 123.456,
                            "data_json": {"json": "json"},
                        },
                    },
                ],
                "id": 29,
                "name": "Campaign-29",
                "percentTraffic": 100,
                "key": "FR_T_100_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FR_T_100_WW": {
        "sdkKey": "someuniquestuff1234567",
        "groups": {},
        "campaignGroups": {},
        "campaigns": [
            {
                "goals": [],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 100,
                        "segments": {"or": [{"custom_variable": {"safari": "true"}}]},
                    }
                ],
                "variables": [{"id": 2, "key": "BOOLEAN_VARIABLE", "type": "boolean", "value": True}],
                "id": 29,
                "percentTraffic": 100,
                "isForcedVariationEnabled": True,
                "key": "FR_T_100_WW",
                "name": "Campaign-24",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT",
                "segments": {},
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FR_WRONG_VARIABLE_TYPE": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [],
                "variations": [{"id": "1", "name": "Control", "weight": 100}],
                "variables": [
                    # STRING:
                    {"id": 1, "key": "STRING_TO_INTEGER", "type": "integer", "value": "123"},
                    {"id": 2, "key": "STRING_TO_FLOAT", "type": "double", "value": "123.456"},
                    # STRING_TO_BOOLEAN NOT POSSIBLE
                    # BOLLEAN:
                    {"id": 3, "key": "BOOLEAN_TO_STRING", "type": "string", "value": True},
                    # BOOLEAN TO INT, DOUBLE NOT POSSIBLE
                    # INTEGER:
                    {"id": 4, "key": "INTEGER_TO_STRING", "type": "string", "value": 24},
                    {"id": 5, "key": "INTEGER_TO_FLOAT", "type": "double", "value": 24},
                    # INTEGER TO BOOLEAN NOT POSSIBLE
                    # FLOAT:
                    {"id": 6, "key": "FLOAT_TO_STRING", "type": "string", "value": 24.24},
                    {"id": 7, "key": "FLOAT_TO_INTEGER", "type": "integer", "value": 24.0},
                    # FLOAT TO BOOLEAN NOT POSSIBLE
                    # JSON:
                    {"id": 8, "key": "JSON_STRING_TO_JSON", "type": "json", "value": '{"json": "json"}'},
                    # JSON TO BOOLEAN, INT, DOUBLE NOT POSSIBLE
                    # WRONG CASES
                    {"id": 9, "key": "WRONG_BOOLEAN", "type": "boolean", "value": "True"},
                    {"id": 10, "key": "WRONG_JSON_1", "type": "json", "value": True},
                    {"id": 11, "key": "WRONG_JSON_2", "type": "json", "value": "this_is_a_string"},
                    {"id": 12, "key": "WRONG_JSON_3", "type": "json", "value": 123},
                    {"id": 13, "key": "WRONG_JSON_4", "type": "json", "value": 123.234},
                ],
                "id": 29,
                "name": "Campaign-29",
                "percentTraffic": 100,
                "key": "FR_WRONG_VARIABLE_TYPE",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FT_T_0_W_10_20_30_40": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "FEATURE_TEST_GOAL", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Control string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                        ],
                        "isFeatureEnabled": False,
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-1 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 456},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-2 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 789},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-3 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 100},
                        ],
                        "isFeatureEnabled": True,
                    },
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 0,
                "key": "FT_T_0_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FT_T_25_W_10_20_30_40": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "FEATURE_TEST_GOAL", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Control string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                        ],
                        "isFeatureEnabled": False,
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-1 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 456},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-2 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 789},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-3 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 100},
                        ],
                        "isFeatureEnabled": True,
                    },
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 25,
                "key": "FT_T_25_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FT_T_50_W_10_20_30_40": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "FEATURE_TEST_GOAL", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Control string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                        ],
                        "isFeatureEnabled": False,
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-1 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 456},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-2 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 789},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-3 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 100},
                        ],
                        "isFeatureEnabled": True,
                    },
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 50,
                "key": "FT_T_50_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FT_T_75_W_10_20_30_40": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "FEATURE_TEST_GOAL", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Control string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                        ],
                        "isFeatureEnabled": False,
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-1 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 456},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-2 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 789},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-3 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 100},
                        ],
                        "isFeatureEnabled": True,
                    },
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 75,
                "key": "FT_T_75_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FT_T_100_W_10_20_30_40": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "FEATURE_TEST_GOAL", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Control string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                        ],
                        "isFeatureEnabled": False,
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-1 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 456},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-2 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 789},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-3 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 100},
                        ],
                        "isFeatureEnabled": True,
                    },
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 100,
                "key": "FT_T_100_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "FT_T_100_W_10_20_30_40_IFEF": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "FEATURE_TEST_GOAL", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Control string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                        ],
                        "isFeatureEnabled": False,
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-1 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 456},
                        ],
                        "isFeatureEnabled": False,
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-2 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 789},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-3 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 100},
                        ],
                        "isFeatureEnabled": False,
                    },
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 100,
                "key": "FT_T_100_W_10_20_30_40_IFEF",
                "status": "RUNNING",
                "type": "FEATURE_TEST",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "NEW_SETTINGS_FILE": {
        "campaigns": [
            {
                "goals": [],
                "variations": [{"id": "1", "name": "Control", "weight": 100}],
                "variables": [
                    {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "d1"},
                    {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                ],
                "id": 29,
                "name": "Campaign-29",
                "percentTraffic": 50,
                "key": "FEATURE_ROLLOUT_KEY",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT",
            },
            {
                "goals": [{"identifier": "FEATURE_TEST_GOAL", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 50,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "d2"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 321},
                        ],
                        "isFeatureEnabled": False,
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 50,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "d1"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                        ],
                        "isFeatureEnabled": True,
                    },
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 50,
                "key": "FEATURE_TEST",
                "status": "RUNNING",
                "type": "FEATURE_TEST",
            },
            {
                "goals": [{"identifier": "CUSTOM_RECOMMENDATION_AB_GOAL", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": "1", "name": "Control", "weight": 40},
                    {"id": "2", "name": "Variation-1", "weight": 60},
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 90,
                "key": "NEW_RECOMMENDATION_AB_CAMPAIGN",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            },
        ],
        "accountId": 123456,
        "version": 2,
    },
    "T_75_W_10_TIMES_10": {
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 231, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 10},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 10},
                    {"id": 3, "name": "Variation-2", "changes": {}, "weight": 10},
                    {"id": 4, "name": "Variation-3", "changes": {}, "weight": 10},
                    {"id": 5, "name": "Variation-4", "changes": {}, "weight": 10},
                    {"id": 6, "name": "Variation-5", "changes": {}, "weight": 10},
                    {"id": 7, "name": "Variation-6", "changes": {}, "weight": 10},
                    {"id": 8, "name": "Variation-7", "changes": {}, "weight": 10},
                    {"id": 9, "name": "Variation-8", "changes": {}, "weight": 10},
                    {"id": 10, "name": "Variation-9", "changes": {}, "weight": 10},
                ],
                "id": 260,
                "name": "Campaign-260",
                "percentTraffic": 75,
                "key": "T_75_W_10_TIMES_10",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "T_100_W_50_50_WS": {
        "sdkKey": "some_unique_key",
        "campaigns": [
            {
                "percentTraffic": 100,
                "goals": [{"identifier": "ddd", "id": 453, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 174,
                "name": "Campaign-174",
                "segments": {
                    "and": [
                        {"or": [{"custom_variable": {"a": "wildcard(*123*)"}}]},
                        {"or": [{"custom_variable": {"hello": "regex(world)"}}]},
                    ]
                },
                "key": "T_100_W_50_50_WS",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "T_50_W_50_50_WS": {
        "sdkKey": "some_unique_key",
        "campaigns": [
            {
                "percentTraffic": 50,
                "goals": [{"identifier": "ddd", "id": 453, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 174,
                "name": "Campaign-174",
                "segments": {
                    "and": [
                        {"or": [{"custom_variable": {"a": "wildcard(*123*)"}}]},
                        {"or": [{"custom_variable": {"hello": "regex(world)"}}]},
                    ]
                },
                "key": "T_50_W_50_50_WS",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "FT_T_75_W_10_20_30_40_WS": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "FEATURE_TEST_GOAL", "id": 203, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Control string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 123},
                        ],
                        "isFeatureEnabled": False,
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-1 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 456},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-2 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 789},
                        ],
                        "isFeatureEnabled": True,
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "Variation-3 string"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 100},
                        ],
                        "isFeatureEnabled": True,
                    },
                ],
                "id": 22,
                "name": "Campaign-22",
                "percentTraffic": 75,
                "key": "FT_T_75_W_10_20_30_40_WS",
                "status": "RUNNING",
                "type": "FEATURE_TEST",
                "segments": {
                    "and": [
                        {"or": [{"custom_variable": {"a": "wildcard(*123*)"}}]},
                        {"or": [{"custom_variable": {"hello": "regex(world)"}}]},
                    ]
                },
            }
        ],
        "accountId": 123456,
        "version": 2,
    },
    "T_100_W_33_33_33_WS_WW": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 218, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": 1,
                        "name": "Control",
                        "changes": {},
                        "weight": 33.3333,
                        "segments": {"or": [{"custom_variable": {"safari": "true"}}]},
                    },
                    {
                        "id": 2,
                        "name": "Variation-1",
                        "changes": {},
                        "weight": 33.3333,
                        "segments": {"or": [{"custom_variable": {"browser": "wildcard(chrome*)"}}]},
                    },
                    {
                        "id": 3,
                        "name": "Variation-2",
                        "changes": {},
                        "weight": 33.3333,
                        "segments": {"or": [{"custom_variable": {"chrome": "false"}}]},
                    },
                ],
                "id": 235,
                "name": "Campaign-235",
                "percentTraffic": 100,
                "key": "T_100_W_33_33_33_WS_WW",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "isForcedVariationEnabled": True,
                "segments": {
                    "and": [
                        {"or": [{"custom_variable": {"contains_vwo": "wildcard(*vwo*)"}}]},
                        {
                            "and": [
                                {
                                    "and": [
                                        {
                                            "or": [
                                                {
                                                    "and": [
                                                        {
                                                            "or": [
                                                                {
                                                                    "and": [
                                                                        {
                                                                            "or": [
                                                                                {
                                                                                    "custom_variable": {
                                                                                        "regex_for_all_letters": "regex(^[A-z]+$)"
                                                                                    }
                                                                                }
                                                                            ]
                                                                        },
                                                                        {
                                                                            "or": [
                                                                                {
                                                                                    "custom_variable": {
                                                                                        "regex_for_capital_letters": "regex(^[A-Z]+$)"
                                                                                    }
                                                                                }
                                                                            ]
                                                                        },
                                                                    ]
                                                                },
                                                                {
                                                                    "or": [
                                                                        {
                                                                            "custom_variable": {
                                                                                "regex_for_small_letters": "regex(^[a-z]+$)"
                                                                            }
                                                                        }
                                                                    ]
                                                                },
                                                            ]
                                                        },
                                                        {
                                                            "or": [
                                                                {
                                                                    "custom_variable": {
                                                                        "regex_for_no_zeros": "regex(^[1-9]+$)"
                                                                    }
                                                                }
                                                            ]
                                                        },
                                                    ]
                                                },
                                                {"or": [{"custom_variable": {"regex_for_zeros": "regex(^[0]+$)"}}]},
                                            ]
                                        },
                                        {"or": [{"custom_variable": {"regex_real_number": "regex(^\\d+(\\.\\d+)?)"}}]},
                                    ]
                                },
                                {
                                    "or": [
                                        {"or": [{"custom_variable": {"this_is_regex": "regex(this\\s+is\\s+text)"}}]},
                                        {
                                            "and": [
                                                {
                                                    "and": [
                                                        {
                                                            "or": [
                                                                {
                                                                    "custom_variable": {
                                                                        "starts_with": "wildcard(starts_with_variable*)"
                                                                    }
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "or": [
                                                                {
                                                                    "custom_variable": {
                                                                        "contains": "wildcard(*contains_variable*)"
                                                                    }
                                                                }
                                                            ]
                                                        },
                                                    ]
                                                },
                                                {
                                                    "or": [
                                                        {
                                                            "not": {
                                                                "or": [
                                                                    {
                                                                        "custom_variable": {
                                                                            "is_not_equal_to": "is_not_equal_to_variable"
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            "or": [
                                                                {
                                                                    "custom_variable": {
                                                                        "is_equal_to": "equal_to_variable"
                                                                    }
                                                                }
                                                            ]
                                                        },
                                                    ]
                                                },
                                            ]
                                        },
                                    ]
                                },
                            ]
                        },
                    ]
                },
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "FT_100_W_33_33_33_WS_WW": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 218, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {
                        "id": 1,
                        "name": "Control",
                        "changes": {},
                        "weight": 33.3333,
                        "segments": {"or": [{"custom_variable": {"safari": "true"}}]},
                        "isFeatureEnabled": False,
                        "variables": [
                            {"id": 1, "key": "STRING_VARIABLE", "type": "string", "value": "CONTROL_STRING_VARIABLE"},
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 0},
                            {"id": 3, "key": "FLOAT_VARIABLE", "type": "double", "value": 0.0},
                            {
                                "id": 4,
                                "key": "JSON_VARIABLE",
                                "type": "json",
                                "value": {"data": "CONTROL_JSON_VARIABLE"},
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "name": "Variation-1",
                        "changes": {},
                        "weight": 33.3333,
                        "segments": {"or": [{"custom_variable": {"browser": "wildcard(chrome*)"}}]},
                        "isFeatureEnabled": True,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "VARIATION-1_STRING_VARIABLE",
                            },
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 1},
                            {"id": 3, "key": "FLOAT_VARIABLE", "type": "double", "value": 1.1},
                            {
                                "id": 4,
                                "key": "JSON_VARIABLE",
                                "type": "json",
                                "value": {"data": "VARIATION-1_JSON_VARIABLE"},
                            },
                        ],
                    },
                    {
                        "id": 3,
                        "name": "Variation-2",
                        "changes": {},
                        "weight": 33.3333,
                        "segments": {"or": [{"custom_variable": {"chrome": "false"}}]},
                        "isFeatureEnabled": False,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "VARIATION-2_STRING_VARIABLE",
                            },
                            {"id": 2, "key": "INTEGER_VARIABLE", "type": "integer", "value": 2},
                            {"id": 3, "key": "FLOAT_VARIABLE", "type": "double", "value": 2.2},
                            {
                                "id": 4,
                                "key": "JSON_VARIABLE",
                                "type": "json",
                                "value": {"data": "VARIATION-2_JSON_VARIABLE"},
                            },
                        ],
                    },
                ],
                "id": 235,
                "name": "Campaign-235",
                "percentTraffic": 100,
                "key": "FT_100_W_33_33_33_WS_WW",
                "status": "RUNNING",
                "type": "FEATURE_TEST",
                "isForcedVariationEnabled": True,
                "segments": {
                    "and": [
                        {"or": [{"custom_variable": {"contains_vwo": "wildcard(*vwo*)"}}]},
                        {
                            "and": [
                                {
                                    "and": [
                                        {
                                            "or": [
                                                {
                                                    "and": [
                                                        {
                                                            "or": [
                                                                {
                                                                    "and": [
                                                                        {
                                                                            "or": [
                                                                                {
                                                                                    "custom_variable": {
                                                                                        "regex_for_all_letters": "regex(^[A-z]+$)"
                                                                                    }
                                                                                }
                                                                            ]
                                                                        },
                                                                        {
                                                                            "or": [
                                                                                {
                                                                                    "custom_variable": {
                                                                                        "regex_for_capital_letters": "regex(^[A-Z]+$)"
                                                                                    }
                                                                                }
                                                                            ]
                                                                        },
                                                                    ]
                                                                },
                                                                {
                                                                    "or": [
                                                                        {
                                                                            "custom_variable": {
                                                                                "regex_for_small_letters": "regex(^[a-z]+$)"
                                                                            }
                                                                        }
                                                                    ]
                                                                },
                                                            ]
                                                        },
                                                        {
                                                            "or": [
                                                                {
                                                                    "custom_variable": {
                                                                        "regex_for_no_zeros": "regex(^[1-9]+$)"
                                                                    }
                                                                }
                                                            ]
                                                        },
                                                    ]
                                                },
                                                {"or": [{"custom_variable": {"regex_for_zeros": "regex(^[0]+$)"}}]},
                                            ]
                                        },
                                        {"or": [{"custom_variable": {"regex_real_number": "regex(^\\d+(\\.\\d+)?)"}}]},
                                    ]
                                },
                                {
                                    "or": [
                                        {"or": [{"custom_variable": {"this_is_regex": "regex(this\\s+is\\s+text)"}}]},
                                        {
                                            "and": [
                                                {
                                                    "and": [
                                                        {
                                                            "or": [
                                                                {
                                                                    "custom_variable": {
                                                                        "starts_with": "wildcard(starts_with_variable*)"
                                                                    }
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "or": [
                                                                {
                                                                    "custom_variable": {
                                                                        "contains": "wildcard(*contains_variable*)"
                                                                    }
                                                                }
                                                            ]
                                                        },
                                                    ]
                                                },
                                                {
                                                    "or": [
                                                        {
                                                            "not": {
                                                                "or": [
                                                                    {
                                                                        "custom_variable": {
                                                                            "is_not_equal_to": "is_not_equal_to_variable"
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            "or": [
                                                                {
                                                                    "custom_variable": {
                                                                        "is_equal_to": "equal_to_variable"
                                                                    }
                                                                }
                                                            ]
                                                        },
                                                    ]
                                                },
                                            ]
                                        },
                                    ]
                                },
                            ]
                        },
                    ]
                },
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "GLOBAL_TRACK_SETTINGS_FILE": {
        "accountId": 88888888,
        "campaigns": [
            {
                "goals": [
                    {"id": 1, "identifier": "track1", "type": "CUSTOM_GOAL"},
                    {"id": 2, "identifier": "track2", "type": "CUSTOM_GOAL"},
                    {"id": 3, "identifier": "track3", "type": "REVENUE_TRACKING"},
                    {"id": 4, "identifier": "track4", "type": "REVENUE_TRACKING"},
                ],
                "id": 1,
                "name": "Campaign-1",
                "isForcedVariationEnabled": False,
                "key": "global_test_1",
                "percentTraffic": 100,
                "segments": {},
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "variations": [
                    {"changes": {}, "id": 1, "name": "Control", "weight": 33.3333},
                    {"changes": {}, "id": 2, "name": "Variation-1", "weight": 33.3333},
                    {"changes": {}, "id": 3, "name": "Variation-2", "weight": 33.3333},
                ],
            },
            {
                "goals": [
                    {"id": 1, "identifier": "track1", "type": "CUSTOM_GOAL"},
                    {"id": 3, "identifier": "track3", "type": "CUSTOM_GOAL"},
                    {"id": 2, "identifier": "track2", "type": "REVENUE_TRACKING"},
                    {"id": 4, "identifier": "track4", "type": "REVENUE_TRACKING"},
                ],
                "id": 2,
                "name": "Campaign-2",
                "isForcedVariationEnabled": False,
                "key": "feature_test_1",
                "percentTraffic": 100,
                "segments": {},
                "status": "RUNNING",
                "type": "FEATURE_TEST",
                "variations": [
                    {
                        "changes": {},
                        "id": 1,
                        "isFeatureEnabled": False,
                        "name": "Control",
                        "variables": [{"id": 1, "key": "string_1", "type": "string", "value": "default"}],
                        "weight": 50,
                    },
                    {
                        "changes": {},
                        "id": 2,
                        "isFeatureEnabled": True,
                        "name": "Variation-1",
                        "variables": [{"id": 1, "key": "string_1", "type": "string", "value": "default"}],
                        "weight": 50,
                    },
                ],
            },
        ],
        "sdkKey": "someuniquestuff1234567",
        "version": 1,
    },
    "VALIDATE_EXTRA_PARAM_IN_CAMPAIGN": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "isExtraParamPresentInValidation": True,
                "id": 230,
                "name": "Campaign-230",
                "percentTraffic": 50,
                "key": "AB_T_50_W_50_50",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "VALIDATE_EXTRA_PARAM_IN_ROOT": {
        "sdkKey": "someuniquestuff1234567",
        "isExtraParamPresentInValidation": True,
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 230,
                "name": "Campaign-230",
                "percentTraffic": 50,
                "key": "AB_T_50_W_50_50",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "NEW_BUCKET_ALGO": {
        "isNB": True,
        "sdkKey": "someuniquestuff1234567",
        "isExtraParamPresentInValidation": True,
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control-Old", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1-Old", "changes": {}, "weight": 50},
                ],
                "isOB": True,
                "id": 230,
                "name": "Campaign-230",
                "percentTraffic": 100,
                "key": "NEW_BUCKET_ALGO_OLD_CAMPAIGN",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            },
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control-New", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1-New", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "name": "Campaign-231",
                "percentTraffic": 100,
                "key": "NEW_BUCKET_ALGO_NEW_CAMPAIGN",
                "status": "RUNNING",
                "type": "VISUAL_AB",
            },
        ],
        "accountId": 88888888,
        "version": 1,
    },
    "SETTINGS_WITHOUT_SEED_WITHOUT_ISOB": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "percentTraffic": 100,
                "name": "BUCKET_ALGO_WITHOUT_SEED",
                "key": "BUCKET_ALGO_WITHOUT_SEED",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
            }
        ],
        "accountId": 888888,
        "version": 1,
        "isNB": True,
    },
    "SETTINGS_WITH_SEED_WITHOUT_ISOB": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "percentTraffic": 100,
                "isBucketingSeedEnabled": True,
                "name": "BUCKET_ALGO_WITH_SEED",
                "key": "BUCKET_ALGO_WITH_SEED",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
            }
        ],
        "accountId": 888888,
        "version": 1,
        "isNB": True,
    },
    "SETTINGS_WITH_ISNB_WITH_ISOB": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "percentTraffic": 100,
                "isBucketingSeedEnabled": True,
                "name": "BUCKET_ALGO_WITH_SEED_WITH_isNB_WITH_isOB",
                "key": "BUCKET_ALGO_WITH_SEED_WITH_isNB_WITH_isOB",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
                "isOB": True,
            }
        ],
        "accountId": 888888,
        "version": 1,
        "isNB": True,
    },
    "SETTINGS_WITH_ISNB_WITHOUT_ISOB": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "percentTraffic": 100,
                "isBucketingSeedEnabled": True,
                "name": "BUCKET_ALGO_WITH_SEED_WITH_isNB_WITHOUT_isOB",
                "key": "BUCKET_ALGO_WITH_SEED_WITH_isNB_WITHOUT_isOB",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
            }
        ],
        "accountId": 888888,
        "version": 1,
        "isNB": True,
    },
    "SETTINGS_WITHOUT_SEED_WITH_ISNB_WITHOUT_ISOB": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "percentTraffic": 100,
                "name": "BUCKET_ALGO_WITH_SEED_WITH_isNB_WITHOUT_isOB",
                "key": "BUCKET_ALGO_WITH_SEED_WITH_isNB_WITHOUT_isOB",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
            }
        ],
        "accountId": 888888,
        "version": 1,
        "isNB": True,
    },
    "SETTINGS_MEGNEW_ONLY_PRIORITY": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "percentTraffic": 100,
                "name": "MEGNEW_ONLY_PRIORITY_0",
                "key": "MEGNEW_ONLY_PRIORITY_0",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
            },
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 232,
                "percentTraffic": 100,
                "name": "MEGNEW_ONLY_PRIORITY_1",
                "key": "MEGNEW_ONLY_PRIORITY_1",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
            },
        ],
        "accountId": 888888,
        "version": 1,
        "groups": {"1": {"name": "group1", "campaigns": [231, 232], "et": 2, "p": [231, 232]}},
        "campaignGroups": {"231": 1, "232": 1},
    },
    "SETTINGS_MEGNEW_ONLY_TRAFFIC": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "percentTraffic": 100,
                "name": "MEGNEW_ONLY_TRAFFIC_0",
                "key": "MEGNEW_ONLY_TRAFFIC_0",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
            },
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 232,
                "percentTraffic": 100,
                "name": "MEGNEW_ONLY_TRAFFIC_1",
                "key": "MEGNEW_ONLY_TRAFFIC_1",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
            },
        ],
        "accountId": 888888,
        "version": 1,
        "groups": {"1": {"name": "group1", "campaigns": [231, 232], "et": 2, "wt": {"231": 80, "232": 20}}},
        "campaignGroups": {"231": 1, "232": 1},
    },
    "SETTINGS_FILE_EVENTPROPERTIES": {
        "sdkKey": "someuniquestuff1234567",
        "campaigns": [
            {
                "goals": [
                    {"identifier": "track1", "id": 1, "type": "CUSTOM_GOAL"},
                    {"identifier": "track2", "id": 2, "type": "CUSTOM_GOAL"},
                    {"identifier": "track3", "id": 3, "type": "REVENUE_TRACKING", "revenueProp": "abcd"},
                    {"identifier": "track4", "id": 4, "type": "REVENUE_TRACKING", "mca": -1},
                ],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 231,
                "percentTraffic": 100,
                "name": "track",
                "key": "track",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "segments": {},
            }
        ],
        "accountId": 888888,
        "version": 1,
        "groups": {},
        "campaignGroups": {},
        "isEventArchEnabled": True,
    },
    "VALIDATE_USERSTORAGE_WITH_MAB": {
        "sdkKey": "someuniquestuff1234567",
        "isExtraParamPresentInValidation": True,
        "campaigns": [
            {
                "goals": [{"identifier": "CUSTOM", "id": 213, "type": "CUSTOM_GOAL"}],
                "variations": [
                    {"id": 1, "name": "Control", "changes": {}, "weight": 50},
                    {"id": 2, "name": "Variation-1", "changes": {}, "weight": 50},
                ],
                "id": 230,
                "name": "Campaign-230",
                "percentTraffic": 100,
                "key": "VALIDATE_USERSTORAGE_WITH_MAB",
                "status": "RUNNING",
                "type": "VISUAL_AB",
                "isMAB": True,
            }
        ],
        "accountId": 88888888,
        "version": 1,
    },
}
