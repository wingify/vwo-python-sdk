""" Validate methods and parameters passed to the SDK """

import json
import jsonschema
from ..schemas.settings_file_schema import SETTINGS_FILE_SCHEMA

services = {
    'logger': ['log'],
    'event_dispatcher': ['dispatch'],
    'user_storage': ['get', 'set']
}


def is_valid_settings_file(settings_file):
    """ Validates the project settings_file

    Args:
        settings_file (json):
            JSON object recieved from dacdn server or somewhere else,
            must be json string representation.

    Returns:
        bool: Whether the settings file is valid or not
    """
    try:
        settings_file = json.loads(settings_file)
    except Exception:
        return False
    try:
        jsonschema.validate(
            instance=settings_file,
            schema=SETTINGS_FILE_SCHEMA
        )
    except Exception:
        return False
    return True


def is_valid_service(service, service_name):
    """ Checks whether the service passed by the user
        contains the necessary methods or not

    Args:
        service (classobj): User defined class instance
        service_name (string): Name of the service

    Returns:
        bool: Whether the class instance provided is valid or nont
    """
    service_attributes = services.get(service_name)
    if not service_attributes:
        return False
    for attr in service_attributes:
        if getattr(service, attr, None) is None:
            return False
    return True


def is_valid_value(val):
    return val is not None and bool(val)


def is_valid_number(val):
    return type(val) == int and is_valid_value(val)


def is_valid_string(val):
    return type(val) == str and is_valid_value(val)
