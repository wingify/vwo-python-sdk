GOAL = {
    'items': {
        'type': 'object',
        'properties': {
            'identifier': {
                'type': 'string'
            },
            'id': {
                'type': 'number'
            },
            'type': {
                'type': 'string'
            }
        },
        'required': [
            'identifier',
            'id',
            'type'
        ]
    }
}
