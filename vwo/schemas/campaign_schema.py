from .variation_schema import VARIATION
from .goal_schema import GOAL
from .variable_schema import VARIABLE
from .empty_object_schema import EMPTY_OBJECT


CAMPAIGN = {
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
        'type': {
            'type': ['string']
        },
        'variations': {
            'if': {
                'type': 'array'
            },
            'then': {
                'items': VARIATION
            },
            'else': EMPTY_OBJECT
        },
        'goals': {
            'if': {
                'type': 'array'
            },
            'then': {
                'items': GOAL
            },
            'else': EMPTY_OBJECT
        },
        'variables': {
            'if': {
                'type': 'array',
            },
            'then': {
                'items': VARIABLE
            },
            'else': EMPTY_OBJECT
        }
    },
    'required': [
        'id',
        'key',
        'status',
        'percentTraffic',
        'variations',
        'goals'
    ]
}
