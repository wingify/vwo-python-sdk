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

import os

SDK_NAME = 'vwo-python-sdk'
PLATFORM = 'server'
SEED_VALUE = 1
MAX_TRAFFIC_PERCENT = 100
MAX_TRAFFIC_VALUE = 10000
STATUS_RUNNING = 'RUNNING'
LIBRARY_PATH = os.path.normpath(os.getcwd() + os.sep + os.pardir)
HTTP_PROTOCOL = 'http://'
HTTPS_PROTOCOL = 'https://'


class ENDPOINTS:
    BASE_URL = 'dev.visualwebsiteoptimizer.com'
    ACCOUNT_SETTINGS = '/server-side/settings'
    TRACK_USER = '/server-side/track-user'
    TRACK_GOAL = '/server-side/track-goal'


class EVENTS:
    TRACK_USER = 'track-user'
    TRACK_GOAL = 'track-goal'


class DATA_TYPE:
    NUMBER = 'number'
    STRING = 'string'
    FUNCTION = 'function'
    BOOLEAN = 'boolean'


class API_METHODS:
    CREATE_INSTANCE = 'CREATE_INSTANCE'
    ACTIVATE = 'ACTIVATE'
    GET_VARIATION_NAME = 'GET_VARIATION_NAME'
    TRACK = 'TRACK'


class GOAL_TYPES:
    REVENUE = 'REVENUE_TRACKING'
    CUSTOM = 'CUSTOM_GOAL'


class CAMPAIGN_TYPES:
    VISUAL_AB = 'VISUAL_AB'
    FEATURE_TEST = 'FEATURE_TEST'
    FEATURE_ROLLOUT = 'FEATURE_ROLLOUT'


class VARIABLE_TYPES:
    STRING = 'string'
    INTEGER = 'integer'
    DOUBLE = 'double'
    BOOLEAN = 'boolean'


PY_VARIABLE_TYPES = {
    'string': str,
    'integer': int,
    'double': float,
    'boolean': bool,
}
