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

""" Generic utility for helper math and random functions """

import random
from datetime import datetime
import time
from ..logger import VWOLogger
from ..enums.log_level_enum import LogLevelEnum
from ..enums.log_message_enum import LogMessageEnum

logger = VWOLogger.getInstance()


def get_random_number():
    """Returns a random number

    Returns:
        float: A random number
    """
    return random.random()


def get_current_unix_timestamp():
    """Returns current unix timestamp

    Returns:
        int: Current unix timestamp
    """
    return int(time.mktime(datetime.now().timetuple()))


def get_current_unix_timestamp_milli():
    """Returns current unix timestamp in milliseconds

    Returns:
        int: Current unix timestamp
    """
    return int(time.time() * 1000)


def get_key_value(var):
    """Returns first key value pair of the given dict. Use this only when the dict has one
    key-value pair as python2 and python3 sort dicts in different ways.

    Returns:
        var, var: Tuple of key value pair
    """
    key = next(iter(var))
    value = var[key]
    return key, value


def get_attribute_values(obj):
    """Returns list of attribute values

    Args:
    obj(class): class obj

    Returns:
    attributes(dict): list of attribute values
    """
    return [value for key, value in obj.__dict__.items() if not key.startswith("__")]


def safe_method(method, fail_return_value, FILE):
    """A decoratore to wrap API methods in fail safe manner

    Args:
        method (method): the API method which should be wrapped
        fail_return_value (value): a value which should be returned when the method passed
        fails
        FILE (str): path of the method for logging purpose

    Returns:
        method : a failsafe API method
    """

    def inner_method(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(file=FILE, exception=e))
            return fail_return_value

    return inner_method
