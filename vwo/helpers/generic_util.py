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

""" Generic utility for helper math and random functions """

import random
from datetime import datetime
import time


def get_random_number():
    """ Returns a random number

    Returns:
        float: A random number
    """
    return random.random()


def get_current_unix_timestamp():
    """ Returns current unix timestamp

    Returns:
        int: Current unix timestamp
    """
    return int(time.mktime(datetime.now().timetuple()))


def get_key_value(var):
    """ Returns first key value pair
    of the given dict

    Returns:
        var, var: Tuple of key value pair
    """
    key = next(iter(var))
    value = var[key]
    return key, value
