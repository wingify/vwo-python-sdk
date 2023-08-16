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

""" Utility module for manipulating VWO campaigns """

from __future__ import division
import math
import copy
from ..constants import constants
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger import VWOLogger

FILE = FileNameEnum.Helpers.CampaignUtil


def get_campaign(settings_file, campaign_key):
    """Finds and Returns campaign from given campaign_key.

    Args:
        settings_file (dict): Settings file for the project
        campaign_key (string): Campaign identifier key

    Returns:
        dict: Campaign object
    """

    for campaign in settings_file.get("campaigns"):
        if campaign.get("key") == campaign_key and campaign.get("status") == constants.STATUS_RUNNING:
            return campaign
    VWOLogger.getInstance().log(
        LogLevelEnum.ERROR,
        LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(file=FILE, campaign_key=campaign_key),
    )
    return None


def get_campaigns(settings_file, campaign_keys):
    """Finds and Returns campaign from given campaign_keys.

    Args:
        settings_file (dict): Settings file for the project
        campaign_keys (list): List of Campaign identifier keys

    Returns:
        dict: Dictionary of campaign object mapped to the campaign key
    """
    campaign_key_map = {}
    for campaign in settings_file.get("campaigns"):
        campaign_key_map[campaign.get("key")] = campaign
    found_campaigns = {}
    for campaign_key in campaign_keys:
        if (
            campaign_key_map.get(campaign_key)
            and campaign_key_map.get(campaign_key).get("status") == constants.STATUS_RUNNING
        ):
            found_campaigns[campaign_key] = campaign_key_map.get(campaign_key)
        else:
            VWOLogger.getInstance().log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(file=FILE, campaign_key=campaign_key),
            )
    return found_campaigns


def set_variation_allocation(campaign):
    """Sets variation allocation range in the provided campaign.

    Args:
        campaign (dict): Campaign object
    """
    set_allocation_ranges(campaign.get("variations"))
    for variation in campaign.get("variations"):
        VWOLogger.getInstance().log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.VARIATION_RANGE_ALLOCATION.format(
                file=FILE,
                campaign_key=campaign.get("key"),
                variation_name=variation.get("name"),
                variation_weight=variation.get("weight"),
                start=variation.get("allocation_range_start"),
                end=variation.get("allocation_range_end"),
            ),
        )


def set_allocation_ranges(items):
    """Sets allocation range on each item(variation/campaign) as allocation_range_start
    and allocation_range_end.

    Args:
        items (list): List of item(variation/campaign) objects
    """

    allocation_ranges = get_allocation_ranges(items)
    for i, item in enumerate(items):
        item.update(allocation_range_start=allocation_ranges[i][0], allocation_range_end=allocation_ranges[i][1])


def get_allocation_ranges(items):
    """Returns a list of allocation ranges from the weights of corresponding items.

    Args:
        items (list): List of item(variation/campaign) objects

    Returns:
        list(tuple): list of tuple(start_range, end_range) for each
        variation
    """

    weights = [item.get("weight") for item in items]
    current_allocation = 0
    allocation_ranges = []
    for weight in weights:
        step_factor = _get_bucketing_range(weight)
        if step_factor:
            start_range = current_allocation + 1
            end_range = current_allocation + step_factor
            allocation_ranges.append((start_range, end_range))
            current_allocation += step_factor
        else:
            allocation_ranges.append((-1, -1))
    return allocation_ranges


def _get_bucketing_range(weight):
    """Returns the bucket size of variation.

    Args:
        weight (int|float): weight of variation

    Returns:
        int: Bucket start range of Variation
    """

    if weight is None or weight == 0:
        return 0
    start_range = int(math.ceil(weight * 100))
    return min(start_range, constants.MAX_TRAFFIC_VALUE)


def get_campaigns_with_goal_id(campaigns, goal_identifer):
    """Returns campaigns having the same goal_identifier passed in the args
    from the campaigns list

    Args:
        campaigns (list): List of campaign objects
        gaol_identifier (str): Global goal identifier

    Returns:
        tuple (campaign_goal_list, campaigns_without_goal): campaign_goal_list is a tuple
        of (campaign, campaign_goal)
    """
    campaign_goal_list = []
    campaigns_without_goal = []
    for campaign in campaigns:
        campaign_goal = get_campaign_goal(campaign, goal_identifer)
        if campaign_goal:
            campaign_goal_list.append((campaign, campaign_goal))
        else:
            campaigns_without_goal.append(campaign)
    return campaign_goal_list, campaigns_without_goal


def get_campaign_goal(campaign, goal_identifier):
    """Returns goal from given campaign and Goal_identifier.

    Args:
        campaign (dict): The running campaign
        goal_identifier (string): Goal identifier

    Returns:
        dict: Goal corresponding to goal_identifer in respective campaign
    """

    if not campaign or not goal_identifier:
        return None
    for goal in campaign.get("goals"):
        if goal.get("identifier") == goal_identifier:
            return goal
    return None


def get_campaign_variation(campaign, variation_name):
    """Returns variation from given campaign and variation_name.

    Args:
        campaign (dict): The running campaign
        variation_name (string): Variation identifier

    Returns:
        dict: Variation corresponding to variation_name in respective campaign
    """

    if not campaign or not variation_name:
        return None
    for variation in campaign.get("variations"):
        if variation.get("name") == variation_name:
            return variation
    return None


def get_variable(variables, variable_key):
    """Returns variable from given variables list.

    Args:
        variables (list): List of variables, whether in campaigns or
        inside variation
        variable_key (string): Variable identifier

    Returns:
        dict: Variable corresponding to variable_key in given variable list
    """
    for variable in variables:
        if variable.get("key") == variable_key:
            return variable
    return None


def get_control_variation(campaign):
    """Returns control variation from a given campaign

    Args:
        campaign (dict): Running campaign
    Returns:
        variation (dict): Control variation from the campaign, ie having id = 1
    """

    for variation in campaign.get("variations"):
        if int(variation.get("id")) == 1:
            return variation
    return None


def scale_variations(variations):
    """It extracts the weights from all the variations inside the campaign
    and scales them so that the total sum of eligible variations' weights become 100%

    Args:
        variations(list): list of variations(dict object) having weight as a property
    """
    weight_sum = sum(variation.get("weight") for variation in variations)
    if weight_sum == 0:
        normalized_weight = 100 / len(variations)
        for variation in variations:
            variation["weight"] = normalized_weight
    else:
        for variation in variations:
            variation["weight"] = (variation["weight"] / weight_sum) * 100


def scale_campaigns(campaigns):
    """It extracts the weights from all the campaigns and scales them so that
    the total sum of eligible campaigns' weights become 100%.

    Args:
        campaigns(list): list of campaigns(dict object) having weight as a property
    """

    normalized_weight = 100 / len(campaigns)
    for campaign in campaigns:
        campaign["weight"] = normalized_weight


def is_part_of_group(settings_file, campaign_id):
    """Checks whether a campaign is part of a group.

    Args:
        settings_file (dict): Settings file for the project
        campaign_id (int): Id of campaign which is to be checked

    Returns:
        bool: True if campaign part of any group else False
    """
    campaignGroups = settings_file.get("campaignGroups")
    if campaignGroups and str(campaign_id) in campaignGroups:
        return True
    return False


def get_group_campaigns(settings_file, group_id):
    """Returns campaigns which are part of given group using group_id.

    Args:
        settings_file (dict): Settings file for the project
        group_id (int): id of group whose campaigns are to be return

    Returns:
        group_campaigns (list): campaigns part of given group
    """
    group_campaign_ids = []
    group_campaigns = []

    groups = settings_file.get("groups")
    if groups and str(group_id) in groups:
        group_campaign_ids = groups.get(str(group_id)).get("campaigns")

    if group_campaign_ids:
        for campaign_id in group_campaign_ids:
            for campaign in settings_file.get("campaigns"):
                if campaign.get("id") == campaign_id and campaign.get("status") == constants.STATUS_RUNNING:
                    group_campaigns.append(copy.copy(campaign))

    return group_campaigns


def get_bucketing_seed(is_new_bucketing_enabled, user_id, campaign=None, group_id=None):
    """Decide the Seed for murmurhash to bucket user.

    Args:
        user_id (string): ID assigned to a user
        campaign (dict): Campaign object
        group_id (int): group id if called campaign is part of group

    Returns:
        string: user seed for generating hash for bucketing variation/campaigns
    """

    if group_id:
        return str(group_id) + "_" + user_id
    elif campaign and (is_new_bucketing_enabled or campaign.get("isBucketingSeedEnabled")):
        return str(campaign.get("id")) + "_" + user_id

    return user_id
