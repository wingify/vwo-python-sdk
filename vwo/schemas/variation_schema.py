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
