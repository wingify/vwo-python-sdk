""" Validate basic things """

import json
import jsonschema
from .schemas import SETTINGS_FILE_SCHEMA

utilities = {
    'logger': ['log'],
    'event_dispatcher': ['dispatch'],
    'user_profile_service': ['lookup', 'save']
}


def _has_method(obj, method):
    """ Checks whether the object contains the specified method or not

    Args:
        obj (classobj|instance):
            Class obj in which the method presence should be checked
        method (function): Function to be checked

    Returns:
        bool : Whether the specified method exists in the object or not
    """
    return getattr(obj, method, None) is not None


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
    except Exception as e:
        return False
    try:
        jsonschema.validate(
            instance=settings_file,
            schema=SETTINGS_FILE_SCHEMA
        )
    except jsonschema.exceptions.SchemaError as e:
        print('Settings File Schema not properly defined', e)
        return False
    except jsonschema.exceptions.ValidationError as e:
        print('Settings File Validation error', e)
        return False
    return True


def is_valid_utility(utility, utility_name):
    """ Checks whether the utility passed by the user
        contains the necessary methods or not

    Args:
        utility (classobj): User defined class instance
        utility_name (string): Name of the utility

    Returns:
        bool: Whether the class instance provided is valid or nont
    """
    utility_attributes = utilities.get(utility_name)
    if not utility_attributes:
        return False
    for attr in utility_attributes:
        if not _has_method(utility, attr):
            return False
    return True


def is_valid_value(val):
    return val is not None and bool(val)


def is_valid_number(val):
    return type(val) == int and is_valid_value(val)


def is_valid_string(val):
    return type(val) == str and is_valid_value(val)


def is_valid_instance(val):
    return str(type(val)) == "<type 'instance'>" and is_valid_value(val)


def is_valid_classobj(val):
    return str(type(val)) == "<type 'classobj'>" and is_valid_value(val)


def is_valid_function(val):
    return str(type(val)) == "<type 'function'>" and is_valid_value(val)


def is_valid_boolean(val):
    return str(type(val)) == "<type 'bool'>"

# def activate(campaign_test_key, user_id):
#     return [
#         dict(
#             key = 'campaign_test_key',
#             value = campaign_test_key,
#             type = CONSTANTS.DATA_TYPE.NUMBER
#         ),
#         dict(
#             key = 'user_id',
#             value = user_id,
#             type = CONSTANTS.DATA_TYPE.NUMBER
#         )
#     ]
# globals()[CONSTANTS.API_METHODS.ACTIVATE] = activate

# def track(campaign_test_key, user_id, gaol_identifier):
#     return [
#         dict(
#             key = 'campaign_test_key',
#             value = campaign_test_key,
#             type = CONSTANTS.DATA_TYPE.NUMBER
#         ),
#         dict(
#             key = 'user_id',
#             value = user_id,
#             type = CONSTANTS.DATA_TYPE.NUMBER
#         ),
#         dict(
#             key = 'gaol_identifier',
#             value = gaol_identifier,
#             type = CONSTANTS.DATA_TYPE.NUMBER
#         )
#     ]
# globals()[CONSTANTS.API_METHODS.TRACK] = track

# def are_valid_param_for_api_method(
#   method,
#   campaign_test_key,
#   user_id,
#   goal_identifier
# ):
#     is_valid = False
#     args = globals()[method](campaign_test_key, user_id, goal_identifier)
