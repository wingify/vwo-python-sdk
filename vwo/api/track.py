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

from ..helpers import impression_util
from ..constants import constants
from ..constants.constants import API_METHODS
from ..helpers import campaign_util, validate_util
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum

FILE = FileNameEnum.Api.Track


def _track(vwo_instance, campaign_key, user_id, goal_identifier, kwargs={}):
    """
    This API method: Marks the conversion of the campaign
    for a particular goal

    1. validates the arguments being passed
    2. Checks if user is eligible to get bucketed into the campaign,
    3. Gets the assigned determinitic variation to the
        user(based on userId), if user becomes part of campaign
    4. Sends an impression call to VWO server to track goal data

    Args:
        campaign_key (string): unique campaign key
        user_id (string): ID assigned to a user
        goal_identifier (string): unique campaign's goal identifier
        revenue_value (int|float|string): Provide it through **kwargs.
        It is the revenue generated on triggering the goal
        custom_variables (dict): Pass it through **kwargs as custom_variables={},
        Custom variables required for segmentation
    """

    vwo_instance.logger.set_api(API_METHODS.TRACK)
    # Retrive revenue value and custom_variables
    revenue_value = kwargs.get('revenue_value')
    custom_variables = kwargs.get('custom_variables')
    variation_targeting_variables = kwargs.get('variation_targeting_variables')

    # Check for valid args
    if not validate_util.is_valid_string(campaign_key) \
        or not validate_util.is_valid_string(user_id) \
            or not validate_util.is_valid_string(goal_identifier) \
            or (custom_variables is not None and not validate_util.is_valid_dict(custom_variables)) \
            or (variation_targeting_variables is not None and  # noqa: W504
            not validate_util.is_valid_dict(variation_targeting_variables)) \
            or (revenue_value is not None and not validate_util.is_valid_basis_data_type(revenue_value)):  # noqa: E501
        # log invalid params
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.TRACK_API_INVALID_PARAMS.format(
                file=FILE
            )
        )
        return False

    if not vwo_instance.is_valid:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.API_CONFIG_CORRUPTED.format(
                file=FILE
            )
        )
        return False

    # Get the campaign settings
    campaign = campaign_util.get_campaign(vwo_instance.settings_file, campaign_key)

    # Validate campaign
    if not campaign or campaign.get('status') != constants.STATUS_RUNNING:
        # log error
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(
                file=FILE,
                campaign_key=campaign_key,
            )
        )
        return False

    campaign_type = campaign.get('type')

    if campaign_type == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                file=FILE,
                user_id=user_id,
                campaign_key=campaign_key,
                campaign_type=campaign_type
            )
        )
        return False

    variation = vwo_instance.variation_decider.get_variation(user_id,
                                                             campaign,
                                                             custom_variables=custom_variables,
                                                             variation_targeting_variables=variation_targeting_variables)  # noqa: E501

    if variation:
        goal = campaign_util.get_campaign_goal(campaign, goal_identifier)
        if not goal:
            vwo_instance.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.TRACK_API_GOAL_NOT_FOUND.format(
                    file=FILE,
                    goal_identifier=goal_identifier,
                    user_id=user_id,
                    campaign_key=campaign_key,
                )
            )
            return False
        elif goal.get('type') == constants.GOAL_TYPES.REVENUE and \
                not validate_util.is_valid_value(revenue_value):
            vwo_instance.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.TRACK_API_REVENUE_NOT_PASSED_FOR_REVENUE_GOAL.format(
                    file=FILE,
                    user_id=user_id,
                    goal_identifier=goal_identifier,
                    campaign_key=campaign_key,
                )
            )
            return False

        if goal.get('type') == constants.GOAL_TYPES.CUSTOM:
            revenue_value = None

        impression = impression_util.create_impression(vwo_instance.settings_file,
                                                       campaign.get('id'),
                                                       variation.get('id'),
                                                       user_id,
                                                       goal.get('id'),
                                                       revenue_value)

        vwo_instance.event_dispatcher.dispatch(impression)

        vwo_instance.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.MAIN_KEYS_FOR_IMPRESSION.format(
                file=FILE,
                campaign_id=impression.get('experiment_id'),
                user_id=impression.get('uId'),
                account_id=impression.get('account_id'),
                variation_id=impression.get('combination')
            )
        )
        return True
    return False
