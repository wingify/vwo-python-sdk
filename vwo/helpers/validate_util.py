# Copyright 2019 Wingify Software Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    """ Validates the settings_file

    Args:
        settings_file (json):
            JSON object received from our server or somewhere else,
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
        bool: Whether the class instance provided is valid or not
    """
    service_attributes = services.get(service_name)
    if not service_attributes:
        return False
    for attr in service_attributes:
        if getattr(service, attr, None) is None:
            return False
    return True


def is_valid_log_level(level):
    string_levels = [
        'CRITICAL',
        'FATAL',
        'ERROR',
        'WARN',
        'WARNING',
        'INFO',
        'DEBUG',
        'NOTSET',
    ]
    if isinstance(level, str) and level not in string_levels:
        return False
    else:
        return is_valid_number(level)


def is_valid_dict(val):
    return type(val) is dict


def is_valid_value(val):
    return val is not None and bool(val)


def is_valid_non_zero_number(val):
    return type(val) == int and is_valid_value(val)


def is_valid_number(val):
    return type(val) == int


def is_valid_string(val):
    return type(val) == str and is_valid_value(val)


def is_valid_basis_data_type(val):
    return type(val) in [int, float, bool, str]
