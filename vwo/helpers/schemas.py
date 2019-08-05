""" Schema for verifying the settings_file provided by the customer """

SETTINGS_FILE_SCHEMA = {
    'type': 'object',
    'properties': {
        'version': {
            'type': ['number', 'string']
        },
        'accountId': {
            'type': ['number', 'string']
        },
        'campaigns': {
            'if': {
                'type': 'array'
            },
            'then': {
                'minItems': 1,
                'items': {
                    '$ref': '#/definitions/campaign_object_schema'
                }
            },
            'else': {
                'type': 'object',
                'maxProperties': 0
            }
        }
    },
    'definitions': {
        'campaign_variation_schema': {
            'type': 'object',
            'properties': {
                'id': {
                    'type': ['number', 'string']
                },
                'name': {
                    'type': ['string']
                },
                'weight': {
                    'type': ['number', 'string']
                }
            },
            'required': [
                'id',
                'name',
                'weight'
            ]
        },
        'campaign_object_schema': {
            'type': 'object',
            'properties': {
                'id': {
                    'type': ['number', 'string']
                },
                'key': {
                    'type': ['string']
                },
                'status': {
                    'type': ['string']
                },
                'percentTraffic': {
                    'type': ['number']
                },
                'variations': {
                    'type': 'array',
                    'items': {
                        '$ref': '#/definitions/campaign_variation_schema'
                    },
                    'minItems': 2
                }
            },
            'required': [
                'id',
                'key',
                'status',
                'percentTraffic',
                'variations'
            ]
        }
    },
    'required': [
        'version',
        'accountId',
        'campaigns'
    ]
}
