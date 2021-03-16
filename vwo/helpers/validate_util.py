# Copyright 2019-2021 Wingify Software Pvt. Ltd.
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

import sys
import json
import jsonschema
from ..schemas.settings_file_schema import SETTINGS_FILE_SCHEMA
from ..constants.constants import INTEGRATIONS, LOG_LEVELS, GOAL_TYPES, BATCH_EVENTS
from . import generic_util
from ..logger import VWOLogger
from ..enums.log_level_enum import LogLevelEnum
from ..enums.log_message_enum import LogMessageEnum

services = {"logger": ["log"], "event_dispatcher": ["dispatch"], "user_storage": ["get", "set"], "integrations": ["callback"]}


def is_valid_settings_file(settings_file):
    """ Validates the settings_file

    Args:
        settings_file (json):
            JSON object received from our server or somewhere else,
            must be json string representation.

    Returns:
        bool: Whether the settings_file is valid or not
    """
    try:
        settings_file = json.loads(settings_file)
    except Exception:
        return False
    try:
        jsonschema.validate(instance=settings_file, schema=SETTINGS_FILE_SCHEMA)
    except Exception:
        return False
    return True


def is_valid_service(service, service_name):
    """ Checks whether the service passed by the user contains the necessary methods or not

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
    """ Validates if the value passed is lies inside the vwo.enums.LogLevelEnum enum or not.

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if valid LOG_LEVEL else False
    """
    return level in generic_util.get_attribute_values(LOG_LEVELS)


def is_valid_goal_type(goal_type):
    """ Validates if the value passed is lies inside the vwo.constants.GOAL_TYPE enum or not.

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if valid GOAL_TYPE else False
    """
    return goal_type in generic_util.get_attribute_values(GOAL_TYPES)


def is_valid_dict(val):
    """ Validates if the value passed is of dict type or not.

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if dict else False
    """
    return type(val) is dict


def is_valid_value(val):
    """ Validates if the value passed is a valid value,
    note: None is a valid value

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if not None and bool(val) is True else False
    """
    return val is not None and bool(val)


def is_valid_non_zero_number(val):
    """ Validates if the value passed is a number & it is non zero.

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if nonzero number else False
    """
    return type(val) == int and is_valid_value(val)


def is_valid_number(val):
    """ Validates if the value passed is a number(int/float) or not.

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if number else False
    """
    return type(val) == int


def is_valid_bool(val):
    """ Validates if the value passed is a boolean or not.

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if bool else False
    """
    return type(val) == bool


def is_valid_unicode(val):
    """ Validates if the value passed is a python unicode value or not.

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if unicode else False
    """
    if sys.version_info[0] < 3:
        return type(val) is unicode
    return False


def is_valid_string(val):
    """ Validates if the value passed is a valid python str or not.

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if string else False
    """
    return (type(val) == str or is_valid_unicode(val)) and is_valid_value(val)


def is_valid_basic_data_type(val):
    """ Validates if the value passed is of basic data type or not.

    Args:
        val (any type): value to be tested

    Returns:
        bool: True if basic data type else False
    """
    return type(val) in [int, float, bool, str]


def is_valid_batch_event_settings(val, file):
    """ Validates if the value passed batch_event_settings has correct data type and values or not.

    Args:
        val (dict): value to be tested

    Returns:
        bool: True if all conditions are passed else False
    """
    logger = VWOLogger.getInstance()

    if not is_valid_dict(val):
        logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.EVENT_BATCHING_NOT_OBJECT.format(file=file))
        return False

    events_per_request = val.get(BATCH_EVENTS.EVENTS_PER_REQUEST)
    request_time_interval = val.get(BATCH_EVENTS.REQUEST_TIME_INTERVAL)
    flush_callback = val.get(BATCH_EVENTS.FLUSH_CALLBACK)

    if events_per_request is None and request_time_interval is None:
        logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.EVENT_BATCHING_INSUFFICIENT.format(file=file))
        return False

    if events_per_request is not None and not(type(events_per_request) in [int]):
        logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.EVENTS_PER_REQUEST_INVALID.format(file=file))
        return False

    if request_time_interval is not None and not(type(request_time_interval) in [int, float]):
        logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.REQUEST_TIME_INTERVAL_INVALID.format(file=file))
        return False

    if events_per_request is not None:
        if events_per_request < BATCH_EVENTS.MIN_EVENTS_PER_REQUEST or events_per_request > BATCH_EVENTS.MAX_EVENTS_PER_REQUEST:
            logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.EVENTS_PER_REQUEST_OUT_OF_BOUNDS.format(file=file, min_value=BATCH_EVENTS.MIN_EVENTS_PER_REQUEST, max_value=BATCH_EVENTS.MAX_EVENTS_PER_REQUEST))
            return False

    if request_time_interval is not None:
        if request_time_interval < BATCH_EVENTS.MIN_REQUEST_TIME_INTERVAL:
            logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.REQUEST_TIME_INTERVAL_OUT_OF_BOUNDS.format(file=file, min_value=BATCH_EVENTS.MIN_REQUEST_TIME_INTERVAL))
            return False

    if flush_callback is not None and not callable(flush_callback):
        logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.FLUSH_CALLBACK_INVALID.format(file=file))
        return False

    return True

