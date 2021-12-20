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

FILE = FileNameEnum.Api.Activate


def _activate(vwo_instance, campaign_key, user_id, **kwargs):
    """This API method: Gets the variation assigned for the user
        for the campaign and send the metrics to VWO server

    1. Validates the arguments being passed
    2. Checks if user is eligible to get bucketed into the campaign,
    3. Assigns the determinitic variation to the user(based on userId),
        if user becomes part of campaign
        If UserStorage is used, it will look into it for the
        variation and if found, no further processing is done
    4. Sends an impression call to VWO server to track user

    Args:
        campaign_key (string): unique campaign key
        user_id (string): ID assigned to a user

    Keywork Args:
        custom_variables (dict): Custom variables required for segmentation
        variation_targeting_variables (dict): Whitelisting variables to target users

    Returns:
        strings|None: If variation is assigned then variation-name
        otherwise None in case of user not becoming part
    """

    vwo_instance.logger.set_api(API_METHODS.ACTIVATE)
    # Retrieve custom variables
    custom_variables = kwargs.get("custom_variables")
    variation_targeting_variables = kwargs.get("variation_targeting_variables")

    # Validate input parameters
    if (
        not validate_util.is_valid_string(campaign_key)
        or not validate_util.is_valid_string(user_id)
        or (custom_variables is not None and not validate_util.is_valid_dict(custom_variables))
        or (
            variation_targeting_variables is not None and not validate_util.is_valid_dict(variation_targeting_variables)
        )
    ):  # noqa: E501
        vwo_instance.logger.log(
            LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.ACTIVATE_API_INVALID_PARAMS.format(file=FILE)
        )
        return None

    # Get the campaign settings
    campaign = campaign_util.get_campaign(vwo_instance.settings_file, campaign_key)

    # Validate campaign
    if not campaign:
        return None

    # Get campaign type
    campaign_type = campaign.get("type")

    # Validate valid api call
    if campaign_type != constants.CAMPAIGN_TYPES.VISUAL_AB:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                file=FILE, user_id=user_id, campaign_key=campaign_key, campaign_type=campaign_type
            ),
        )
        return None

    # Once the matching RUNNING campaign is found, assign the
    # deterministic variation to the user_id provided
    variation, is_user_tracked = vwo_instance.variation_decider.get_variation(
        user_id,
        campaign,
        custom_variables=custom_variables,
        variation_targeting_variables=variation_targeting_variables,
        api_method=constants.API_METHODS.ACTIVATE,
    )  # noqa: E501

    # Check if variation_name has been assigned
    if not variation:
        return None

    if is_user_tracked is False:

        if not vwo_instance.is_event_arch_enabled or vwo_instance.is_event_batching_enabled is True:
            # Variation found, dispatch event to our servers
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
            params = impression_util.get_events_params(vwo_instance.settings_file, constants.EVENTS.VWO_VARIATION_SHOWN)
            impression = impression_util.create_track_user_events_impression(
                vwo_instance.settings_file, campaign.get("id"), variation.get("id"), user_id
            )
            vwo_instance.event_dispatcher.dispatch_events(params=params, impression=impression)

    else:
        vwo_instance.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.USER_ALREADY_TRACKED.format(
                file=FILE, user_id=user_id, campaign_key=campaign_key, api_method=constants.API_METHODS.ACTIVATE
            ),
        )

    return variation.get("name")
