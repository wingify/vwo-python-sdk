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
from ..helpers import campaign_util, validate_util, feature_util
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum

FILE = FileNameEnum.Api.GetFeatureVariableValue


def _get_feature_variable_value(vwo_instance, campaign_key, variable_key, user_id, **kwargs):
    """Returns the feature variable corresponding to the variable_key
    passed. It typecasts the value to the corresponding value type
    found in settings_file

    1. Validates the arguments being passed
    2. Checks if user is eligible to get bucketed into the feature test/rollout,
    3. Assigns the determinitic variation to the user(based on userId),
        if user becomes part of campaign
        If UserStorage is used, it will look into it for the
            variation and if found, no further processing is done
    4. Retrieves the corresponding variable from variation assigned.

    Args:
        campaign_key (string): unique campaign key
        variable_key (string): variable key
        user_id (string): ID assigned to a user

    Keywork Args:
        custom_variables (dict): Custom variables required for segmentation
        variation_targeting_variables (dict): Whitelisting variables to target users

    Returns:
        variable(bool, str, int, float)|None: If variation is assigned then
        variable corresponding to variation assigned else None
    """

    vwo_instance.logger.set_api(API_METHODS.GET_FEATURE_VARIABLE_VALUE)
    # Retrieve custom variables
    custom_variables = kwargs.get("custom_variables")
    variation_targeting_variables = kwargs.get("variation_targeting_variables")

    if (
        not validate_util.is_valid_string(campaign_key)
        or not validate_util.is_valid_string(variable_key)
        or not validate_util.is_valid_string(user_id)
        or (custom_variables is not None and not validate_util.is_valid_dict(custom_variables))
        or (
            variation_targeting_variables is not None and not validate_util.is_valid_dict(variation_targeting_variables)
        )
    ):  # noqa: E501
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.GET_FEATURE_VARIABLE_VALUE_API_INVALID_PARAMS.format(file=FILE),
        )
        return None

    # Get the campaign settings
    campaign = campaign_util.get_campaign(vwo_instance.settings_file, campaign_key)

    # Validate campaign
    if not campaign:
        return None

    campaign_type = campaign.get("type")

    if campaign_type == constants.CAMPAIGN_TYPES.VISUAL_AB:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                file=FILE, campaign_key=campaign_key, campaign_type=campaign_type, user_id=user_id
            ),
        )
        return None

    variation, _ = vwo_instance.variation_decider.get_variation(
        user_id,
        campaign,
        custom_variables=custom_variables,
        variation_targeting_variables=variation_targeting_variables,
        api_method=constants.API_METHODS.GET_FEATURE_VARIABLE_VALUE,
    )  # noqa: E501

    # Check if variation has been assigned to user
    if not variation:
        return None

    # Variation received, evaluate variable
    variable = None

    if campaign_type == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
        variables = campaign.get("variables")

    elif campaign_type == constants.CAMPAIGN_TYPES.FEATURE_TEST:
        if variation.get("isFeatureEnabled") is False:
            vwo_instance.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.FEATURE_NOT_ENABLED_FOR_USER.format(
                    file=FILE, feature_key=campaign_key, user_id=user_id
                ),
            )
            variation = campaign_util.get_control_variation(campaign)
        else:
            vwo_instance.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.FEATURE_ENABLED_FOR_USER.format(
                    file=FILE, feature_key=campaign_key, user_id=user_id
                ),
            )
        variables = variation.get("variables")

    variable = campaign_util.get_variable(variables, variable_key)

    if not variable:
        # Log variable not found
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.VARIABLE_NOT_FOUND.format(
                file=FILE,
                variable_key=variable_key,
                campaign_key=campaign_key,
                campaign_type=campaign_type,
                user_id=user_id,
            ),
        )
        return None

    vwo_instance.logger.log(
        LogLevelEnum.INFO,
        LogMessageEnum.INFO_MESSAGES.VARIABLE_FOUND.format(
            file=FILE,
            variable_key=variable_key,
            variable_value=variable.get("value"),
            campaign_key=campaign_key,
            campaign_type=campaign_type,
            user_id=user_id,
        ),
    )

    return feature_util.get_type_casted_feature_value(variable.get("value"), variable.get("type"))
