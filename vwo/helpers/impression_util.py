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
    from urllib.parse import quote  # Python 3+

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
