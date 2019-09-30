""" Helper utility that creates an impression to send to server """

import json
import pkg_resources
from ..constants import constants
from ..helpers import function_util, uuid_util, validate_util
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger.logger_manager import VWOLogger
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+


def create_impression(
    settings_file,
    campaign_id,
    variation_id,
    user_id,
    goal_id=None,
    revenue=None
):
    """ Creates the impression from the arguments passed according to
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

    if (not validate_util.is_valid_number(campaign_id) or not
            validate_util.is_valid_string(user_id)):
        return None

    is_track_user_api = True
    if goal_id is not None:
        is_track_user_api = False
    account_id = settings_file.get('accountId')

    impression = dict(
        account_id=account_id,
        experiment_id=campaign_id,
        ap=constants.PLATFORM,
        uId=quote(user_id.encode("utf-8")),
        combination=variation_id,
        random=function_util.get_random_number(),
        sId=function_util.get_current_unix_timestamp(),
        u=uuid_util.generator_for(user_id, account_id)
    )
    # Version and SDK constants
    impression['sdk'] = 'python'
    impression['sdk-v'] = pkg_resources.require(constants.SDK_NAME)[0].version

    url = constants.HTTPS_PROTOCOL + constants.ENDPOINTS.BASE_URL
    logger = VWOLogger.getInstance()

    if is_track_user_api:
        impression.update(ed=json.dumps({'p': 'server'}))
        impression.update(url=url + constants.ENDPOINTS.TRACK_USER)
        logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.IMPRESSION_FOR_TRACK_USER.format(
                file=FileNameEnum.ImpressionUtil,
                properties=json.dumps(impression)
            )
        )
    else:
        impression.update(url=url + constants.ENDPOINTS.TRACK_GOAL)
        impression.update(goal_id=goal_id)
        if revenue:
            impression.update(r=revenue)
        logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.IMPRESSION_FOR_TRACK_GOAL.format(
                file=FileNameEnum.ImpressionUtil,
                properties=json.dumps(impression)
            )
        )
    return impression
