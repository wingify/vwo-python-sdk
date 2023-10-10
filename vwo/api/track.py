# Copyright 2019-2022 Wingify Software Pvt. Ltd.
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


def _track(vwo_instance, campaign_specifier, user_id, goal_identifier, **kwargs):
    """
    This API method: Marks the conversion of the campaign(s) for a particular goal

    1. validates the arguments being passed
    2. retrieves the campaigns having the same global goal
    3. calls track_campaign_goal for all the goals

    Args:
        campaign_specifier (None, list, string): Campaign key(s), it can be None in case
        of all campaigns, list in case of given campaigns and string in case of particular
        campaign should to be tracked.
        user_id (string): ID assigned to a user
        goal_identifier (string): campaign(s)'s unique goal identifier

    Keyword Args:
        revenue_value (int|float|string): Provide it through **kwargs.
        It is the revenue generated on triggering the goal
        custom_variables (dict): Custom variables required for segmentation
        variation_targeting_variables (dict): Whitelisting variables to target users

    Returns:
        dict|None: None if called for single campaign and no goal tracked or
        called for all campaigns and no goal tracked.
        Dict otherwise of campaign_key with True/False showing whether the goal
        has been tracked for the campaign or not
    """

    vwo_instance.logger.set_api(API_METHODS.TRACK)

    if vwo_instance.is_opted_out:
        vwo_instance.logger.log(
            LogLevelEnum.INFO, LogMessageEnum.INFO_MESSAGES.API_NOT_ENABLED.format(file=FILE, api=API_METHODS.TRACK)
        )

        return None

    # Retrive revenue value and custom_variables
    revenue_value = kwargs.get("revenue_value")
    custom_variables = kwargs.get("custom_variables")
    user_agent = kwargs.get("user_agent")
    user_ip_address = kwargs.get("user_ip_address")
    variation_targeting_variables = kwargs.get("variation_targeting_variables")
    event_properties = kwargs.get("event_properties")
    valid_params = True
    # Check for valid args
    if (
        not validate_util.is_valid_string(user_id)
        or not validate_util.is_valid_string(goal_identifier)
        or (custom_variables is not None and not validate_util.is_valid_dict(custom_variables))
        or (
            variation_targeting_variables is not None and not validate_util.is_valid_dict(variation_targeting_variables)
        )
        or (revenue_value is not None and not validate_util.is_valid_basic_data_type(revenue_value))
    ):
        valid_params = False

    goal_type_to_track = kwargs.get("goal_type_to_track")
    if goal_type_to_track is None:
        goal_type_to_track = vwo_instance.goal_type_to_track
    elif not validate_util.is_valid_goal_type(goal_type_to_track):
        valid_params = False

    if not valid_params:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.TRACK_API_INVALID_PARAMS.format(file=FILE)
        )
        return None

    campaigns_without_goal = []
    no_campaign_found = False
    if type(campaign_specifier) is str:
        campaign = campaign_util.get_campaign(vwo_instance.settings_file, campaign_specifier)
        goal = campaign_util.get_campaign_goal(campaign, goal_identifier)
        if not goal:
            no_campaign_found = True
        else:
            campaign_goal_list = [(campaign, goal)]
    elif type(campaign_specifier) is list:
        campaigns = campaign_util.get_campaigns(vwo_instance.settings_file, campaign_specifier).values()
        (campaign_goal_list, campaigns_without_goal) = campaign_util.get_campaigns_with_goal_id(
            campaigns, goal_identifier
        )
        for campaign in campaigns_without_goal:
            vwo_instance.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.TRACK_API_GOAL_NOT_FOUND.format(
                    file=FILE, goal_identifier=goal_identifier, user_id=user_id, campaign_key=campaign.get("key")
                ),
            )
    elif campaign_specifier is None:
        campaigns = vwo_instance.settings_file.get("campaigns")
        campaign_goal_list = campaign_util.get_campaigns_with_goal_id(campaigns, goal_identifier)[0]
        if not campaign_goal_list:
            no_campaign_found = True
    else:
        vwo_instance.logger.log(
            # Specific log for campaign_specifier type
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.TRACK_API_INVALID_PARAMS.format(file=FILE),
        )
        return None

    if no_campaign_found:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.NO_CAMPAIGN_FOUND.format(file=FILE, goal_identifier=goal_identifier),
        )
        return None

    ret_value = {}
    campaign_goal_revenue_prop_list = []
    for campaign, goal in campaign_goal_list:
        # check if user storage attached if MAB activated for campaign
        if campaign.get("isMAB") and vwo_instance.variation_decider.user_storage is None:
            vwo_instance.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.NO_USERSTORAGE_WITH_MAB.format(
                    file=FILE, campaign_key=campaign.get("key")
                ),
            )
            ret_value[campaign.get("key")] = False
            continue

        result = track_campaign_goal(
            vwo_instance,
            campaign,
            user_id,
            goal,
            revenue_value,
            custom_variables,
            variation_targeting_variables,
            goal_type_to_track,
            campaign_goal_revenue_prop_list,
            event_properties,
            user_agent,
            user_ip_address,
        )
        ret_value[campaign.get("key")] = result
    for campaign in campaigns_without_goal:
        ret_value[campaign.get("key")] = False

    if len(campaign_goal_revenue_prop_list) != 0 and (
        not vwo_instance.is_event_batching_enabled and vwo_instance.is_event_arch_enabled is True
    ):
        params = impression_util.get_events_params(
            vwo_instance.settings_file, goal_identifier, user_agent=user_agent, user_ip_address=user_ip_address
        )
        impression = impression_util.create_track_goal_events_impression(
            vwo_instance.settings_file,
            user_id,
            goal_identifier,
            campaign_goal_revenue_prop_list,
            event_properties,
            revenue=revenue_value,
        )
        vwo_instance.event_dispatcher.dispatch_events(params=params, impression=impression)

    return ret_value


def track_campaign_goal(
    vwo_instance,
    campaign,
    user_id,
    goal,
    revenue_value,
    custom_variables,
    variation_targeting_variables,
    goal_type_to_track,
    campaign_goal_revenue_prop_list,
    event_properties,
    user_agent,
    user_ip_address,
):
    """
    It marks the conversion of given goal for the given campaign

    1. Checks if user is eligible to get bucketed into the campaign,
    2. Gets the assigned determinitic variation to the
        user(based on userId), if user becomes part of campaign
    3. Sends an impression call to VWO server to track goal data if event arch
        is not enabled

    Args:
        campaign (dict): Campaign object
        user_id (string): ID assigned to a user
        goal (dict): Goal object
        revenue_value (int|float|string): It is the revenue generated on triggering the goal
        custom_variables (dict): Custom variables required for segmentation
        variation_targeting_variables (dict): Whitelisting variables to target users
        goal_type_to_track (vwo.GOAL_TYPES): Goal type that should be tracked in case of mixed
        global goal identifier
        campaign_goal_revenue_prop_list (list): list of campaign_id, goal_id & goal's revenueProp
            (if revenue goal else None) to build event arch impression

    Returns:
        bool: True if goal successfully tracked else False
    """

    campaign_type = campaign.get("type")
    if campaign_type == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                file=FILE, user_id=user_id, campaign_key=campaign.get("key"), campaign_type=campaign_type
            ),
        )
        return False

    goal_type = goal.get("type")

    if (goal_type_to_track == constants.GOAL_TYPES.CUSTOM and goal_type == constants.GOAL_TYPES.REVENUE) or (
        goal_type_to_track == constants.GOAL_TYPES.REVENUE and goal_type == constants.GOAL_TYPES.CUSTOM
    ):
        # We can log goal type didn't match in debug mode
        return False

    if goal_type == constants.GOAL_TYPES.REVENUE and not validate_util.is_valid_value(revenue_value):
        if vwo_instance.is_event_arch_enabled is True:
            # If it's a metric of type - value of an event property and calculation logic is first Value (mca != -1)
            if goal.get("mca") != -1:
                # In this case it is expected that goal will have revenueProp
                # Error should be logged if eventProperties is not Defined OR eventProperties does not have revenueProp key
                if event_properties is None or goal.get("revenueProp") not in event_properties:
                    vwo_instance.logger.log(
                        LogLevelEnum.ERROR,
                        LogMessageEnum.ERROR_MESSAGES.TRACK_API_REVENUE_NOT_PASSED_FOR_REVENUE_GOAL.format(
                            file=FILE,
                            user_id=user_id,
                            goal_identifier=goal.get("identifier"),
                            campaign_key=campaign.get("key"),
                        ),
                    )
                    return False
            else:
                # here mca == -1 so there could only be 2 scenarios,
                # 1. If revenueProp is defined then eventProperties should have revenueProp key
                # 2. if revenueProp is not defined then it's a metric of type - Number of times an event has been triggered.
                if goal.get("revenueProp"):
                    # Error should be logged if eventProperties is not Defined OR eventProperties does not have revenueProp key
                    if event_properties is None or goal.get("revenueProp") not in event_properties:
                        vwo_instance.logger.log(
                            LogLevelEnum.ERROR,
                            LogMessageEnum.ERROR_MESSAGES.TRACK_API_REVENUE_NOT_PASSED_FOR_REVENUE_GOAL.format(
                                file=FILE,
                                user_id=user_id,
                                goal_identifier=goal.get("identifier"),
                                campaign_key=campaign.get("key"),
                            ),
                        )
                        return False
        else:
            vwo_instance.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.TRACK_API_REVENUE_NOT_PASSED_FOR_REVENUE_GOAL.format(
                    file=FILE, user_id=user_id, goal_identifier=goal.get("identifier"), campaign_key=campaign.get("key")
                ),
            )
            return False

    if goal_type == constants.GOAL_TYPES.CUSTOM:
        revenue_value = None

    variation, _ = vwo_instance.variation_decider.get_variation(
        user_id,
        campaign,
        custom_variables=custom_variables,
        variation_targeting_variables=variation_targeting_variables,
        goal_data={"identifier": goal.get("identifier"),"mca": goal.get("mca"),"hasProps": goal.get("hasProps")},
        api_method=constants.API_METHODS.TRACK,
    )

    if variation:
        if not vwo_instance.is_event_arch_enabled or vwo_instance.is_event_batching_enabled is True:
            impression = impression_util.create_impression(
                vwo_instance,
                campaign.get("id"),
                variation.get("id"),
                user_id,
                event_properties,
                goal,
                goal.get("id"),
                revenue_value,
                user_agent=user_agent,
                user_ip_address=user_ip_address,
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
            campaign_goal_revenue_prop_list.append((campaign.get("id"), goal.get("id"), goal.get("revenueProp")))

        return True
    return False
