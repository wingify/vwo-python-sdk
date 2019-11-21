# Copyright 2019 Wingify Software Pvt. Ltd.
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

    Campaigns key of each campaign is same as setttings_file name.
"""

SETTINGS_FILES = {
    'EMPTY_SETTINGS_FILE': {},

    'AB_T_50_W_50_50': {
        'sdkKey': 'someuniquestuff1234567',
        'campaigns': [
            {
                'goals': [
                    {
                        'identifier': 'CUSTOM',
                        'id': 213,
                        'type': 'CUSTOM_GOAL'
                    }
                ],
                'variations': [
                    {
                        'id': 1,
                        'name': 'Control',
                        'changes': {},
                        'weight': 50
                    },
                    {
                        'id': 2,
                        'name': 'Variation-1',
                        'changes': {},
                        'weight': 50
                    }
                ],
                'id': 230,
                'percentTraffic': 50,
                'key': 'AB_T_50_W_50_50',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 88888888,
        'version': 1
    },

    'AB_T_100_W_50_50': {
        'sdkKey': 'someuniquestuff1234567',
        'campaigns': [
            {
                'goals': [
                    {
                        'identifier': 'abcd',
                        'id': 1,
                        'type': 'REVENUE_TRACKING'
                    },
                    {
                        'identifier': 'CUSTOM',
                        'id': 214,
                        'type': 'CUSTOM_GOAL'
                    }
                ],
                'variations': [
                    {
                        'id': 1,
                        'name': 'Control',
                        'changes': {},
                        'weight': 50
                    },
                    {
                        'id': 2,
                        'name': 'Variation-1',
                        'changes': {},
                        'weight': 50
                    }
                ],
                'id': 231,
                'percentTraffic': 100,
                'key': 'AB_T_100_W_50_50',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 88888888,
        'version': 1
    },

    'AB_T_100_W_20_80': {
        'sdkKey': 'someuniquestuff1234567',
        'campaigns': [
            {
                'goals': [
                    {
                        'identifier': 'CUSTOM',
                        'id': 215,
                        'type': 'CUSTOM_GOAL'
                    }
                ],
                'variations': [
                    {
                        'id': 1,
                        'name': 'Control',
                        'changes': {},
                        'weight': 20
                    },
                    {
                        'id': 2,
                        'name': 'Variation-1',
                        'changes': {},
                        'weight': 80
                    }
                ],
                'id': 232,
                'percentTraffic': 100,
                'key': 'AB_T_100_W_20_80',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 88888888,
        'version': 1
    },

    'AB_T_20_W_10_90': {
        'sdkKey': 'someuniquestuff1234567',
        'campaigns': [
            {
                'goals': [
                    {
                        'identifier': 'CUSTOM',
                        'id': 216,
                        'type': 'CUSTOM_GOAL'
                    }
                ],
                'variations': [
                    {
                        'id': 1,
                        'name': 'Control',
                        'changes': {},
                        'weight': 10
                    },
                    {
                        'id': 2,
                        'name': 'Variation-1',
                        'changes': {},
                        'weight': 90
                    }
                ],
                'id': 233,
                'percentTraffic': 20,
                'key': 'AB_T_20_W_10_90',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 88888888,
        'version': 1
    },

    'AB_T_100_W_0_100': {
        'sdkKey': 'someuniquestuff1234567',
        'campaigns': [
            {
                'goals': [
                    {
                        'identifier': 'CUSTOM',
                        'id': 217,
                        'type': 'CUSTOM_GOAL'
                    }
                ],
                'variations': [
                    {
                        'id': 1,
                        'name': 'Control',
                        'changes': {},
                        'weight': 0
                    },
                    {
                        'id': 2,
                        'name': 'Variation-1',
                        'changes': {},
                        'weight': 100
                    }
                ],
                'id': 234,
                'percentTraffic': 100,
                'key': 'AB_T_100_W_0_100',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 88888888,
        'version': 1
    },

    'AB_T_100_W_33_33_33': {
        'sdkKey': 'someuniquestuff1234567',
        'campaigns': [
            {
                'goals': [
                    {
                        'identifier': 'CUSTOM',
                        'id': 218,
                        'type': 'CUSTOM_GOAL'
                    }
                ],
                'variations': [
                    {
                        'id': 1,
                        'name': 'Control',
                        'changes': {},
                        'weight': 33.3333
                    },
                    {
                        'id': 2,
                        'name': 'Variation-1',
                        'changes': {},
                        'weight': 33.3333
                    },
                    {
                        'id': 3,
                        'name': 'Variation-2',
                        'changes': {},
                        'weight': 33.3333
                    }
                ],
                'id': 235,
                'percentTraffic': 100,
                'key': 'AB_T_100_W_33_33_33',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 88888888,
        'version': 1
    },

    "DUMMY_SETTINGS_FILE": {
        'sdkKey': 'someuniquestuff1234567',
        'campaigns': [
            {
                'goals': [
                    {
                        'identifier': 'GOAL_NEW',
                        'id': 203,
                        'type': 'CUSTOM_GOAL'
                    }
                ],
                'variations': [
                    {
                        'id': '1',
                        'name': 'Control',
                        'weight': 40
                    },
                    {
                        'id': '2',
                        'name': 'Variation-1',
                        'weight': 60
                    }
                ],
                'id': 22,
                'percentTraffic': 50,
                'key': 'DUMMY_SETTINGS_FILE',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 88888888,
        'version': 1
    },

    'FR_T_0_W_100': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 100
                    }
                ],
                "variables": [
                    {
                        "id": 1,
                        "key": "STRING_VARIABLE",
                        "type": "string",
                        "value": "this_is_a_string"
                    },
                    {
                        "id": 2,
                        "key": "INTEGER_VARIABLE",
                        "type": "integer",
                        "value": 123
                    },
                    {
                        "id": 1,
                        "key": "FLOAT_VARIABLE",
                        "type": "double",
                        "value": 123.456

                    },
                    {
                        "id": 2,
                        "key": "BOOLEAN_VARIABLE",
                        "type": "boolean",
                        "value": True
                    }
                ],
                "id": 29,
                "percentTraffic": 0,
                "key": "FR_T_0_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'FR_T_25_W_100': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 100
                    }
                ],
                "variables": [
                    {
                        "id": 1,
                        "key": "STRING_VARIABLE",
                        "type": "string",
                        "value": "this_is_a_string"

                    },
                    {
                        "id": 2,
                        "key": "INTEGER_VARIABLE",
                        "type": "integer",
                        "value": 123
                    },
                    {
                        "id": 1,
                        "key": "FLOAT_VARIABLE",
                        "type": "double",
                        "value": 123.456

                    },
                    {
                        "id": 2,
                        "key": "BOOLEAN_VARIABLE",
                        "type": "boolean",
                        "value": True
                    }
                ],
                "id": 29,
                "percentTraffic": 25,
                "key": "FR_T_25_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'FR_T_50_W_100': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 100
                    }
                ],
                "variables": [
                    {
                        "id": 1,
                        "key": "STRING_VARIABLE",
                        "type": "string",
                        "value": "this_is_a_string"
                    },
                    {
                        "id": 2,
                        "key": "INTEGER_VARIABLE",
                        "type": "integer",
                        "value": 123
                    },
                    {
                        "id": 1,
                        "key": "FLOAT_VARIABLE",
                        "type": "double",
                        "value": 123.456

                    },
                    {
                        "id": 2,
                        "key": "BOOLEAN_VARIABLE",
                        "type": "boolean",
                        "value": True
                    }
                ],
                "id": 29,
                "percentTraffic": 50,
                "key": "FR_T_50_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'FR_T_75_W_100': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 100
                    }
                ],
                "variables": [
                    {
                        "id": 1,
                        "key": "STRING_VARIABLE",
                        "type": "string",
                        "value": "this_is_a_string"
                    },
                    {
                        "id": 2,
                        "key": "INTEGER_VARIABLE",
                        "type": "integer",
                        "value": 123
                    },
                    {
                        "id": 1,
                        "key": "FLOAT_VARIABLE",
                        "type": "double",
                        "value": 123.456
                    },
                    {
                        "id": 2,
                        "key": "BOOLEAN_VARIABLE",
                        "type": "boolean",
                        "value": True
                    }
                ],
                "id": 29,
                "percentTraffic": 75,
                "key": "FR_T_75_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'FR_T_100_W_100': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 100
                    }
                ],
                "variables": [
                    {
                        "id": 1,
                        "key": "STRING_VARIABLE",
                        "type": "string",
                        "value": "this_is_a_string"
                    },
                    {
                        "id": 2,
                        "key": "INTEGER_VARIABLE",
                        "type": "integer",
                        "value": 123
                    },
                    {
                        "id": 1,
                        "key": "FLOAT_VARIABLE",
                        "type": "double",
                        "value": 123.456
                    },
                    {
                        "id": 2,
                        "key": "BOOLEAN_VARIABLE",
                        "type": "boolean",
                        "value": True
                    }
                ],
                "id": 29,
                "percentTraffic": 100,
                "key": "FR_T_100_W_100",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'FR_WRONG_VARIABLE_TYPE': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 100
                    }
                ],
                "variables": [
                    # STRING:
                    {
                        "id": 1,
                        "key": "STRING_TO_INTEGER",
                        "type": "integer",
                        "value": "123"
                    },
                    {
                        "id": 2,
                        "key": "STRING_TO_FLOAT",
                        "type": "double",
                        "value": "123.456"
                    },
                    # STRING_TO_BOOLEAN NOT POSSIBLE

                    # BOLLEAN:
                    {
                        "id": 3,
                        "key": "BOOLEAN_TO_STRING",
                        "type": "string",
                        "value": True
                    },
                    # BOOLEAN TO INT, DOUBLE NOT POSSIBLE

                    # INTEGER:
                    {
                        "id": 4,
                        "key": "INTEGER_TO_STRING",
                        "type": "string",
                        "value": 24
                    },
                    {
                        "id": 5,
                        "key": "INTEGER_TO_FLOAT",
                        "type": "double",
                        "value": 24
                    },
                    # INTEGER TO BOOLEAN NOT POSSIBLE

                    # FLOAT:
                    {
                        "id": 6,
                        "key": "FLOAT_TO_STRING",
                        "type": "string",
                        "value": 24.24
                    },
                    {
                        "id": 7,
                        "key": "FLOAT_TO_INTEGER",
                        "type": "integer",
                        "value": 24.0
                    },
                    # FLOAT TO BOOLEAN NOT POSSIBLE

                    # WRONG CASES
                    {
                        "id": 8,
                        "key": "WRONG_BOOLEAN",
                        "type": "boolean",
                        "value": "True"
                    },
                ],
                "id": 29,
                "percentTraffic": 100,
                "key": "FR_WRONG_VARIABLE_TYPE",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'FT_T_0_W_10_20_30_40': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [
                    {
                        "identifier": "FEATURE_TEST_GOAL",
                        "id": 203,
                        "type": "CUSTOM_GOAL"
                    }
                ],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Control string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 123
                            }
                        ],
                        "isFeatureEnabled": False
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-1 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 456
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-2 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 789
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-3 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 100
                            }
                        ],
                        "isFeatureEnabled": True
                    }
                ],
                "id": 22,
                "percentTraffic": 0,
                "key": "FT_T_0_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST"
            },
        ],
        "accountId": 123456,
        "version": 2
    },
    'FT_T_25_W_10_20_30_40': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [
                    {
                        "identifier": "FEATURE_TEST_GOAL",
                        "id": 203,
                        "type": "CUSTOM_GOAL"
                    }
                ],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Control string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 123
                            }
                        ],
                        "isFeatureEnabled": False
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-1 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 456
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-2 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 789
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-3 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 100
                            }
                        ],
                        "isFeatureEnabled": True
                    }
                ],
                "id": 22,
                "percentTraffic": 25,
                "key": "FT_T_25_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST"
            },
        ],
        "accountId": 123456,
        "version": 2
    },
    'FT_T_50_W_10_20_30_40': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [
                    {
                        "identifier": "FEATURE_TEST_GOAL",
                        "id": 203,
                        "type": "CUSTOM_GOAL"
                    }
                ],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Control string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 123
                            }
                        ],
                        "isFeatureEnabled": False
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-1 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 456
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-2 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 789
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-3 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 100
                            }
                        ],
                        "isFeatureEnabled": True
                    }
                ],
                "id": 22,
                "percentTraffic": 50,
                "key": "FT_T_50_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'FT_T_75_W_10_20_30_40': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [
                    {
                        "identifier": "FEATURE_TEST_GOAL",
                        "id": 203,
                        "type": "CUSTOM_GOAL"
                    }
                ],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Control string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 123
                            }
                        ],
                        "isFeatureEnabled": False
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-1 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 456
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-2 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 789
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-3 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 100
                            }
                        ],
                        "isFeatureEnabled": True
                    }
                ],
                "id": 22,
                "percentTraffic": 75,
                "key": "FT_T_75_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'FT_T_100_W_10_20_30_40': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [
                    {
                        "identifier": "FEATURE_TEST_GOAL",
                        "id": 203,
                        "type": "CUSTOM_GOAL"
                    }
                ],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Control string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 123
                            }
                        ],
                        "isFeatureEnabled": False
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-1 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 456
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-2 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 789
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-3 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 100
                            }
                        ],
                        "isFeatureEnabled": True
                    }
                ],
                "id": 22,
                "percentTraffic": 100,
                "key": "FT_T_100_W_10_20_30_40",
                "status": "RUNNING",
                "type": "FEATURE_TEST"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'FT_T_100_W_10_20_30_40_IFEF': {
        'sdkKey': 'someuniquestuff1234567',
        "campaigns": [
            {
                "goals": [
                    {
                        "identifier": "FEATURE_TEST_GOAL",
                        "id": 203,
                        "type": "CUSTOM_GOAL"
                    }
                ],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 10,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Control string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 123
                            }
                        ],
                        "isFeatureEnabled": False
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 20,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-1 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 456
                            }
                        ],
                        "isFeatureEnabled": False
                    },
                    {
                        "id": "3",
                        "name": "Variation-2",
                        "weight": 30,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-2 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 789
                            }
                        ],
                        "isFeatureEnabled": True
                    },
                    {
                        "id": "4",
                        "name": "Variation-3",
                        "weight": 40,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "Variation-3 string"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 100
                            }
                        ],
                        "isFeatureEnabled": False
                    }
                ],
                "id": 22,
                "percentTraffic": 100,
                "key": "FT_T_100_W_10_20_30_40_IFEF",
                "status": "RUNNING",
                "type": "FEATURE_TEST"
            },
        ],
        "accountId": 123456,
        "version": 2
    },

    'NEW_SETTINGS_FILE': {
        "campaigns": [
            {
                "goals": [],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 100
                    }
                ],
                "variables": [
                    {
                        "id": 1,
                        "key": "STRING_VARIABLE",
                        "type": "string",
                        "value": "d1"
                    },
                    {
                        "id": 2,
                        "key": "INTEGER_VARIABLE",
                        "type": "integer",
                        "value": 123
                    }
                ],
                "id": 29,
                "percentTraffic": 50,
                "key": "FEATURE_ROLLOUT_KEY",
                "status": "RUNNING",
                "type": "FEATURE_ROLLOUT"
            },
            {
                "goals": [
                    {
                        "identifier": "FEATURE_TEST_GOAL",
                        "id": 203,
                        "type": "CUSTOM_GOAL"
                    }
                ],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 50,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "d2"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 321
                            }
                        ],
                        "isFeatureEnabled": False
                    }, {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 50,
                        "variables": [
                            {
                                "id": 1,
                                "key": "STRING_VARIABLE",
                                "type": "string",
                                "value": "d1"
                            },
                            {
                                "id": 2,
                                "key": "INTEGER_VARIABLE",
                                "type": "integer",
                                "value": 123
                            }
                        ],
                        "isFeatureEnabled": True
                    }
                ],
                "id": 22,
                "percentTraffic": 50,
                "key": "FEATURE_TEST",
                "status": "RUNNING",
                "type": "FEATURE_TEST"
            },
            {
                "goals": [
                    {
                        "identifier": "CUSTOM_RECOMMENDATION_AB_GOAL",
                        "id": 203,
                        "type": "CUSTOM_GOAL"
                    }
                ],
                "variations": [
                    {
                        "id": "1",
                        "name": "Control",
                        "weight": 40
                    },
                    {
                        "id": "2",
                        "name": "Variation-1",
                        "weight": 60
                    }
                ],
                "id": 22,
                "percentTraffic": 90,
                "key": "NEW_RECOMMENDATION_AB_CAMPAIGN",
                "status": "RUNNING",
                "type": "VISUAL_AB"
            }
        ],
        "accountId": 123456,
        "version": 2
    },

    "T_75_W_10_TIMES_10": {
        "campaigns": [
            {
                "goals": [
                    {
                        "identifier": "CUSTOM",
                        "id": 231,
                        "type": "CUSTOM_GOAL"
                    }
                ],
                "variations": [
                    {
                        "id": 1,
                        "name": "Control",
                        "changes": {},
                        "weight": 10
                    },
                    {
                        "id": 2,
                        "name": "Variation-1",
                        "changes": {},
                        "weight": 10
                    },
                    {
                        "id": 3,
                        "name": "Variation-2",
                        "changes": {},
                        "weight": 10
                    },
                    {
                        "id": 4,
                        "name": "Variation-3",
                        "changes": {},
                        "weight": 10
                    },
                    {
                        "id": 5,
                        "name": "Variation-4",
                        "changes": {},
                        "weight": 10
                    },
                    {
                        "id": 6,
                        "name": "Variation-5",
                        "changes": {},
                        "weight": 10
                    },
                    {
                        "id": 7,
                        "name": "Variation-6",
                        "changes": {},
                        "weight": 10
                    },
                    {
                        "id": 8,
                        "name": "Variation-7",
                        "changes": {},
                        "weight": 10
                    },
                    {
                        "id": 9,
                        "name": "Variation-8",
                        "changes": {},
                        "weight": 10
                    },
                    {
                        "id": 10,
                        "name": "Variation-9",
                        "changes": {},
                        "weight": 10
                    }
                ],
                "id": 260,
                "percentTraffic": 75,
                "key": "T_75_W_10_TIMES_10",
                "status": "RUNNING",
                "type": "VISUAL_AB"
            }
        ],
        "accountId": 123456,
        "version": 2
    }
}
