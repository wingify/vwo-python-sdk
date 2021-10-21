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

from ..constants import constants
from ..constants.constants import API_METHODS
from ..helpers import campaign_util, validate_util
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum

FILE = FileNameEnum.Api.GetVariationName


def _get_variation_name(vwo_instance, campaign_key, user_id, **kwargs):
    """This API method: Gets the variation name assigned for the
        user for the campaign

    1. Validates the arguments being passed
    2. Checks if user is eligible to get bucketed into the campaign,
    3. Assigns the determinitic variation to the user(based on userId),
        if user becomes part of campaign
        If UserStorage is used, it will look into it for the
            variation and if found, no further processing is done

    Args:
        campaign_key (string): unique campaign key
        user_id (string): ID assigned to a user

    Keywork Args:
        custom_variables (dict): Custom variables required for segmentation
        variation_targeting_variables (dict): Whitelisting variables to target users

    Returns:
        string|None: If variation is assigned then variation-name
            otherwise None in case of user not becoming part
    """

    vwo_instance.logger.set_api(API_METHODS.GET_VARIATION_NAME)
    # Retrieve custom variables
    custom_variables = kwargs.get("custom_variables")
    variation_targeting_variables = kwargs.get("variation_targeting_variables")

    # Check for valid arguments
    if (
        not validate_util.is_valid_string(campaign_key)
        or not validate_util.is_valid_string(user_id)
        or (custom_variables is not None and not validate_util.is_valid_dict(custom_variables))
        or (
            variation_targeting_variables is not None and not validate_util.is_valid_dict(variation_targeting_variables)
        )
    ):  # noqa: E501
        # log invalid params
        vwo_instance.logger.log(
            LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.GET_VARIATION_NAME_API_INVALID_PARAMS.format(file=FILE)
        )
        return None

    # Get the campaign settings
    campaign = campaign_util.get_campaign(vwo_instance.settings_file, campaign_key)

    # Validate campaign
    if not campaign:
        return None

    campaign_type = campaign.get("type")

    if campaign_type == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                file=FILE, user_id=user_id, campaign_key=campaign_key, campaign_type=campaign_type
            ),
        )
        return None

    variation, _ = vwo_instance.variation_decider.get_variation(
        user_id,
        campaign,
        custom_variables=custom_variables,
        variation_targeting_variables=variation_targeting_variables,
        api_method=constants.API_METHODS.GET_VARIATION_NAME,
    )  # noqa: E501

    # Check if variation_name has been assigned
    if not variation:
        return None

    return variation.get("name")
