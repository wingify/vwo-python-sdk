from .variable_schema import VARIABLE
from .empty_object_schema import EMPTY_OBJECT


VARIATION = {
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
        },
        'variables': {
            'if': {
                'type': 'array',
            },
            'then': {
                'items': VARIABLE
            },
            'else': EMPTY_OBJECT
        },
        'isFeatureEnabled': {
            'type': 'boolean'
        }
    },
    'required': [
        'id',
        'name',
        'weight'
    ]
}
