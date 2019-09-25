# flake8: noqa
""" Schema for verifying the settings_file provided by the customer """

from .campaign_schema import CAMPAIGN
from .empty_object_schema import EMPTY_OBJECT


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
                'items': CAMPAIGN
            },
            'else': EMPTY_OBJECT
        }
    },
    'required': [
        'version',
        'accountId',
        'campaigns'
    ]
}
