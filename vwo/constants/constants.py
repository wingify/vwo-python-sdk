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

import os
import pkg_resources
import logging

SDK_NAME = "vwo-python-sdk"
SDK_VERSION = pkg_resources.require(SDK_NAME)[0].version
API_VERSION = 1
PLATFORM = "server"
SEED_VALUE = 1
MAX_TRAFFIC_PERCENT = 100
MAX_TRAFFIC_VALUE = 10000
STATUS_RUNNING = "RUNNING"
LIBRARY_PATH = os.path.normpath(os.getcwd() + os.sep + os.pardir)
HTTP_PROTOCOL = "http://"
HTTPS_PROTOCOL = "https://"


class ENDPOINTS:
    BASE_URL = "dev.visualwebsiteoptimizer.com"
    ACCOUNT_SETTINGS = "/server-side/settings"
    WEBHOOKS_ACCOUNT_SETTINGS = "/server-side/pull"
    TRACK_USER = "/server-side/track-user"
    TRACK_GOAL = "/server-side/track-goal"
    PUSH = "/server-side/push"
    BATCH_EVENTS = "/server-side/batch-events"
    EVENTS = "/events/t"


class EVENTS:
    TRACK_USER = "track-user"
    TRACK_GOAL = "track-goal"
    PUSH = "push"
    VWO_VARIATION_SHOWN = "vwo_variationShown"
    VWO_SYNC_VISITOR_PROP = "vwo_syncVisitorProp"


class DATA_TYPE:
    NUMBER = "number"
    STRING = "string"
    FUNCTION = "function"
    BOOLEAN = "boolean"


class API_METHODS:
    ACTIVATE = "activate"
    GET_VARIATION_NAME = "get_variation_name"
    TRACK = "track"
    IS_FEATURE_ENABLED = "is_feature_enabled"
    GET_FEATURE_VARIABLE_VALUE = "get_feature_variable_value"
    PUSH = "push"
    FLUSH_EVENTS = "flush_events"
    GET_AND_UPDATE_SETTINGS_FILE = "get_and_update_settings_file"


class GOAL_TYPES:
    REVENUE = "REVENUE_TRACKING"
    CUSTOM = "CUSTOM_GOAL"
    ALL = "ALL"


class BATCH_EVENTS:
    EVENTS_PER_REQUEST = "events_per_request"
    REQUEST_TIME_INTERVAL = "request_time_interval"
    FLUSH_CALLBACK = "flush_callback"
    MAX_EVENTS_PER_REQUEST = 5000
    MIN_EVENTS_PER_REQUEST = 1
    DEFAULT_EVENTS_PER_REQUEST = 100
    DEFAULT_REQUEST_TIME_INTERVAL = 600
    MIN_REQUEST_TIME_INTERVAL = 1


class CAMPAIGN_TYPES:
    VISUAL_AB = "VISUAL_AB"
    FEATURE_TEST = "FEATURE_TEST"
    FEATURE_ROLLOUT = "FEATURE_ROLLOUT"


class INTEGRATIONS:
    CALLBACK = "callback"


class VARIABLE_TYPES:
    STRING = "string"
    INTEGER = "integer"
    DOUBLE = "double"
    BOOLEAN = "boolean"
    JSON = "json"


class PUSH_API:
    TAG_VALUE_LENGTH = 255
    TAG_KEY_LENGTH = 255


PY_VARIABLE_TYPES = {"string": str, "integer": int, "double": float, "boolean": bool, "json": dict}


class SEGMENTATION_TYPES:
    WHITELISTING = "whitelisting"
    PRE_SEGMENTATION = "pre_segmentation"


# For exposing log levels to vwo_instance
class LOG_LEVELS:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
