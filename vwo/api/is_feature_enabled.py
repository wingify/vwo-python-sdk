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

from ..helpers import impression_util
from ..constants import constants
from ..constants.constants import API_METHODS
from ..helpers import campaign_util, validate_util
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum

FILE = FileNameEnum.Api.IsFeatureEnabled


def _is_feature_enabled(vwo_instance, campaign_key, user_id, **kwargs):
    """This API method: Identifies whether the user becomes a part
    of feature rollout/test or not.

    1. Validates the arguments being passed
    2. Checks if user is eligible to get bucketed into the
        feature test/rollout,
    3. Assigns the determinitic variation to the user(based on userId),
        if user becomes part of feature test/rollout
        If UserStorage is used, it will look into it for the
            variation and if found, no further processing is done

    Args:
        campaign_key (string): unique campaign key
        user_id (string): ID assigned to a user

    Keywork Args:
        custom_variables (dict): Custom variables required for segmentation
        variation_targeting_variables (dict): Whitelisting variables to target users
        should_track_returning_user (bool): should returning user be tracked again.

    Returns:
        bool: True if user becomes part of feature test/rollout,
        otherwise false in case user doesn't becomes part of it.
    """

    vwo_instance.logger.set_api(API_METHODS.IS_FEATURE_ENABLED)
    # Retrieve custom variables
    custom_variables = kwargs.get("custom_variables")
    variation_targeting_variables = kwargs.get("variation_targeting_variables")
    should_track_returning_user = kwargs.get("should_track_returning_user")

    if should_track_returning_user is None:
        should_track_returning_user = vwo_instance.should_track_returning_user or False

    if (
        not validate_util.is_valid_string(campaign_key)
        or not validate_util.is_valid_string(user_id)
        or not validate_util.is_valid_bool(should_track_returning_user)
        or (custom_variables is not None and not validate_util.is_valid_dict(custom_variables))
        or (
            variation_targeting_variables is not None and not validate_util.is_valid_dict(variation_targeting_variables)
        )
    ):  # noqa: E501
        # log invalid params
        vwo_instance.logger.log(
            LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.IS_FEATURE_ENABLED_API_INVALID_PARAMS.format(file=FILE)
        )
        return False

    # Get the campaign settings
    campaign = campaign_util.get_campaign(vwo_instance.settings_file, campaign_key)

    # Validate campaign
    if not campaign:
        return False

    # Validate campaign_type
    campaign_type = campaign.get("type")

    if campaign_type == constants.CAMPAIGN_TYPES.VISUAL_AB:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                file=FILE, user_id=user_id, campaign_key=campaign_key, campaign_type=campaign_type
            ),
        )
        return False

    # check if user has already been tracked
    is_user_tracked = vwo_instance.variation_decider.identify_tracked_user_from_user_storage(user_id, campaign_key)

    # Get variation
    variation = vwo_instance.variation_decider.get_variation(
        user_id,
        campaign,
        custom_variables=custom_variables,
        variation_targeting_variables=variation_targeting_variables,
        api_method=constants.API_METHODS.IS_FEATURE_ENABLED,
    )  # noqa: E501

    # If no variation, did not become part of feature_test/rollout
    if not variation:
        return False

    # if campaign type is feature_test Send track call to server
    if campaign_type == constants.CAMPAIGN_TYPES.FEATURE_TEST:
        # track user if user has not already been tracked
        if is_user_tracked is False or should_track_returning_user:
            impression = impression_util.create_impression(
                vwo_instance.settings_file, campaign.get("id"), variation.get("id"), user_id
            )

            vwo_instance.event_dispatcher.dispatch(impression)
            vwo_instance.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.MAIN_KEYS_FOR_IMPRESSION.format(
                    file=FILE,
                    campaign_id=impression.get("experiment_id"),
                    account_id=impression.get("account_id"),
                    variation_id=impression.get("combination"),
                ),
            )
        else:
            vwo_instance.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.USER_ALREADY_TRACKED.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_key=campaign_key,
                    api_method=constants.API_METHODS.IS_FEATURE_ENABLED,
                ),
            )

        result = variation.get("isFeatureEnabled")
        if result:
            vwo_instance.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.FEATURE_ENABLED_FOR_USER.format(
                    file=FILE, user_id=user_id, feature_key=campaign_key
                ),
            )
        else:
            vwo_instance.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.FEATURE_NOT_ENABLED_FOR_USER.format(
                    file=FILE, user_id=user_id, feature_key=campaign_key
                ),
            )
        return result
    return True
