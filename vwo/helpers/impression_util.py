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

""" Helper utility that creates an impression to send to server """

import json
from ..constants import constants
from ..helpers import generic_util, uuid_util, validate_util
from ..services.usage_stats_manager import UsageStats
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger import VWOLogger

try:
    from urllib import quote  # Python 2.X
except ImportError:
    # Python 3+
    from urllib.parse import quote  # noqa: F401

FILE = FileNameEnum.Helpers.ImpressionUtil


def create_impression(settings_file, campaign_id, variation_id, user_id, goal_id=None, revenue=None):
    """Creates the impression from the arguments passed according to
    call type

    Args:
        settings_file (dict): Settings file object
        campaign_id (string): Campaign identifier
        variation_id (string): Variation identifier
        user_id (string): User identifier
        goal_id (string|None): Goal identifier, if building track impression
        revenue (string|float|int|None):
            Number value, in any representation, if building track impression

    Returns:
        None|dict: None if campaign ID or variation ID is invalid,
            else impression(dict)
    """

    if not validate_util.is_valid_non_zero_number(campaign_id) or not validate_util.is_valid_string(user_id):
        return None

    is_track_user_api = True
    if goal_id is not None:
        is_track_user_api = False

    impression = get_common_properties(user_id, settings_file)

    impression.update(experiment_id=campaign_id, combination=variation_id)

    url = constants.HTTPS_PROTOCOL + constants.ENDPOINTS.BASE_URL
    logger = VWOLogger.getInstance()

    if is_track_user_api:
        impression.update(ed=json.dumps({"p": constants.PLATFORM}))
        impression.update(url=url + constants.ENDPOINTS.TRACK_USER)
        impression.update(UsageStats.get_usage_stats())
        logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.IMPRESSION_FOR_TRACK_USER.format(
                file=FILE, properties=get_stringified_log_impression(impression)
            ),
        )
    else:
        impression.update(url=url + constants.ENDPOINTS.TRACK_GOAL)
        impression.update(goal_id=goal_id)
        if revenue:
            impression.update(r=revenue)
        logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.IMPRESSION_FOR_TRACK_GOAL.format(
                file=FILE, properties=get_stringified_log_impression(impression)
            ),
        )
    return impression


def get_common_properties(user_id, settings_file):
    """Returns commonly used params for making requests to our servers.

    Args:
        user_id (string): Unique identification of user
        settings_file: settings file containing campaign data for extracting account_id

    Returns:
        properties(object): commonly used params for making call to our servers
    """

    account_id = settings_file.get("accountId")
    sdk_key = settings_file.get("sdkKey")
    properties = {
        "random": generic_util.get_random_number(),
        "sdk": constants.SDK_NAME,
        "sdk-v": constants.SDK_VERSION,
        "ap": constants.PLATFORM,
        "sId": generic_util.get_current_unix_timestamp(),
        "u": uuid_util.generate_for(user_id, account_id),
        "account_id": account_id,
        "env": sdk_key,
    }
    return properties


def get_stringified_log_impression(impression):
    """Remove sensitive keys from the impression to te displayed in the log.

    Args:
        impression (dict): builted impression

    Returns:
        impression (json_string): stringified impression without sensitive keys
    """
    log_impression = impression.copy()
    log_impression.pop("env")
    return json.dumps(log_impression)


def create_track_user_events_impression(settings_file, campaign_id, variation_id, user_id):
    """Creates the event impression for track user call from the arguments passed accordingly

    Args:
        settings_file (dict): Settings file object
        campaign_id (string): Campaign identifier
        variation_id (string): Variation identifier
        user_id (string): User identifier

    Returns:
        dict: impression for track user
    """
    logger = VWOLogger.getInstance()

    impression = get_events_common_properties(settings_file, user_id, constants.EVENTS.VWO_VARIATION_SHOWN)

    # impression["d"]["event"]["props"].update(UsageStats.get_usage_stats())
    impression["d"]["event"]["props"].update({"id": campaign_id, "variation": variation_id, "isFirst": 1})

    logger.log(
        LogLevelEnum.DEBUG,
        LogMessageEnum.DEBUG_MESSAGES.IMPRESSION_FOR_EVENT_ARCH_TRACK_USER.format(
            file=FILE, account_id=settings_file.get("accountId"), user_id=user_id, campaign_id=campaign_id
        ),
    )

    return impression


def create_track_goal_events_impression(
    settings_file, user_id, goal_identifier, campaign_goal_revenue_prop_list, revenue=None
):
    """Creates the event impression for track goal call from the arguments passed accordingly

    Args:
        settings_file (dict): Settings file object
        user_id (string): User identifier
        goal_identifier (string): campaign(s)'s goal identifier
        campaign_goal_revenue_prop_list (list): list of campaign_id, goal_id & goal's revenueProp
            (if revenue goal else None) to build event arch impression
        revenue (string|float|int): Number value, in any representation

    Returns:
        dict: impression for track goal
    """
    logger = VWOLogger.getInstance()

    impression = get_events_common_properties(settings_file, user_id, goal_identifier)
    impression["d"]["event"]["props"].update({"vwoMeta": {"metric": {}}, "isCustomEvent": True})

    for campaign_id, goal_id, revenue_prop in campaign_goal_revenue_prop_list:
        impression["d"]["event"]["props"]["vwoMeta"]["metric"].update({"id_" + str(campaign_id): ["g_" + str(goal_id)]})

        if revenue_prop and revenue:
            impression["d"]["event"]["props"]["vwoMeta"].update({revenue_prop: revenue})

    logger.log(
        LogLevelEnum.DEBUG,
        LogMessageEnum.DEBUG_MESSAGES.IMPRESSION_FOR_EVENT_ARCH_TRACK_GOAL.format(
            file=FILE,
            goal_identifier=goal_identifier,
            account_id=settings_file.get("accountId"),
            user_id=user_id,
            campaign_ids=[campaign_id for campaign_id, _, _ in campaign_goal_revenue_prop_list],
        ),
    )
    return impression


def create_push_events_impression(settings_file, user_id, custom_dimension_map):
    """Creates the event impression for push call from the arguments passed accordingly

    Args:
        settings_file (dict): Settings file object
        user_id (string): User identifier
        custom_dimension_map (dict|None): Dict of tag keys vs values

    Returns:
        dict: impression for push call
    """
    logger = VWOLogger.getInstance()

    impression = get_events_common_properties(settings_file, user_id, constants.EVENTS.VWO_SYNC_VISITOR_PROP)
    impression["d"]["event"]["props"].update(isCustomEvent=True)

    for tag_key, tag_value in custom_dimension_map.items():
        impression["d"]["event"]["props"]["$visitor"]["props"].update({str(tag_key): str(tag_value)})
        impression["d"]["visitor"]["props"].update({str(tag_key): str(tag_value)})

    logger.log(
        LogLevelEnum.DEBUG,
        LogMessageEnum.DEBUG_MESSAGES.IMPRESSION_FOR_EVENT_ARCH_PUSH.format(
            file=FILE,
            account_id=settings_file.get("accountId"),
            user_id=user_id,
            property=json.dumps(custom_dimension_map),
        ),
    )

    return impression


def get_events_common_properties(settings_file, user_id, event_name):
    """Returns common properties required for making events impression

    Args:
        settings_file (dict): settings file containing campaign data
        user_id (string): User identifier
        event_name (string): name of the event for which request will be made

    Returns:
        dict: common properties dict
    """
    account_id = settings_file.get("accountId")
    sdk_key = settings_file.get("sdkKey")
    uuid = uuid_util.generate_for(user_id, account_id)

    properties = {
        "d": {
            "msgId": uuid + "-" + str(generic_util.get_current_unix_timestamp()),
            "visId": uuid,
            "sessionId": generic_util.get_current_unix_timestamp(),
            "event": {
                "props": {
                    "$visitor": {"props": {"vwo_fs_environment": sdk_key}},
                    "sdkName": constants.SDK_NAME,
                    "sdkVersion": constants.SDK_VERSION,
                },
                "name": event_name,
                "time": generic_util.get_current_unix_timestamp_milli(),
            },
            "visitor": {"props": {"vwo_fs_environment": sdk_key}},
        }
    }

    return properties


def get_events_params(settings_file, event_name):
    """Returns query params for making requests to our servers using events.

    Args:
        settings_file (dict): settings file containing campaign data for extracting account_id & sdk_key
        event_name (string): name of the event for which request will be made

    Returns:
        properties(dict): query params for event call
    """

    account_id = settings_file.get("accountId")
    sdk_key = settings_file.get("sdkKey")
    params = {
        "en": event_name,
        "a": account_id,
        "env": sdk_key,
        "eTime": generic_util.get_current_unix_timestamp_milli(),
        "random": generic_util.get_random_number(),
        "p": "FS",
    }

    if event_name == constants.EVENTS.VWO_VARIATION_SHOWN:
        params.update(UsageStats.get_usage_stats())

    return params
