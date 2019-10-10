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
