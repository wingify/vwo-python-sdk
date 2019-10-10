VARIABLE = {
    'type': 'object',
    'properties': {
        'id': {
            'type': ['number', 'string']
        },
        'key': {
            'type': ['string']
        },
        'value': {
            'type': ['string', 'number', 'boolean']
        },
        'type': {
            'type': ['string']
        }
    },
    'required': [
        'id',
        'value',
        'key',
        'type'
    ]
}
