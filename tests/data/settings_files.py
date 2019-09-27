""" Various settings_file for testings

    Notes:
    Abbreviations: T = percentTraffic
                   W = weight split
                   AB = VISUAL_AB

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
        'accountId': 60781,
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
        'accountId': 60781,
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
        'accountId': 60781,
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
        'accountId': 60781,
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
        'accountId': 60781,
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
        'accountId': 60781,
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
        'accountId': 60781,
        'version': 1
    }
}
