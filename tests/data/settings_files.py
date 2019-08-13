""" Various settings_file for testings """

SETTINGS_FILES = {
    0: {},

    1: {
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
                'key': 'DEV_TEST_1',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 60781,
        'version': 1
    },

    2: {
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
                'key': 'DEV_TEST_2',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 60781,
        'version': 1
    },

    3: {
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
                'key': 'DEV_TEST_3',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 60781,
        'version': 1
    },

    4: {
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
                'key': 'DEV_TEST_4',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 60781,
        'version': 1
    },

    5: {
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
                'key': 'DEV_TEST_5',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 60781,
        'version': 1
    },

    6: {
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
                'key': 'DEV_TEST_6',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 60781,
        'version': 1
    },

    7: {
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
                'key': 'UNIQUE_KEY',
                'status': 'RUNNING',
                'type': 'VISUAL_AB'
            }
        ],
        'accountId': 60781,
        'version': 1
    },
}
