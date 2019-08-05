""" Utitlity module for manipulating VWO campaigns """

import math
from . import constants
from .enums import LogMessageEnum, FileNameEnum, LogLevelEnum
from ..logger import Logger


def get_campaign(settings_file, campaign_test_key):
    """ Finds and Returns campaign from given campaign_test_key.

    Args:
        settings_file (dict): Settings file for the project
        campaign_test_key (string): Campaign identifier key

    Returns:
        dict: Campaign object
    """

    for campaign in settings_file.get('campaigns'):
        if campaign.get('key') == campaign_test_key:
            return campaign
    return None


def set_variation_allocation(campaign):
    """ Sets variation allocation range in the provided campaign.

    Args:
        campaign (dict): Campaign object
    """

    current_allocation = 0
    for variation in campaign.get('variations'):
        step_factor = _get_variation_bucketing_range(variation.get('weight'))
        if step_factor:
            start_range = current_allocation + 1
            end_range = current_allocation + step_factor
            variation.update(start_variation_allocation=start_range,
                             end_variation_allocation=end_range
                             )
            current_allocation += step_factor
        else:
            variation.update(start_variation_allocation=-1,
                             end_variation_allocation=-1
                             )

        Logger().log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.VARIATION_RANGE_ALLOCATION.format(
                file=FileNameEnum.CampaignUtil,
                campaign_test_key=campaign.get('key'),
                variation_name=variation.get('name'),
                variation_weight=variation.get('weight'),
                start=variation.get('start_variation_allocation'),
                end=variation.get('end_variation_allocation')
            )
        )


def _get_variation_bucketing_range(weight):
    """ Returns the bucket size of variation.

    Args:
        weight (int|float): weight of variation

    Returns:
        int: Bucket start range of Variation
    """

    if weight is None or weight == 0:
        return 0
    start_range = int(math.ceil(weight * 100))
    return min(start_range, constants.MAX_TRAFFIC_VALUE)


def get_campaign_goal(settings_file, campaign_test_key, goal_identifier):
    """ Returns goal from given campaign_test_key and gaol_identifier.

    Args:
        settings_file (dict): Settings file of the project
        campaign_test_key (string): Campaign identifier key
        goal_identifier (string): Gaol identifier

    Returns:
        dict: Goal corresponding to gaol_identifer in respective campaign
    """

    if not settings_file or not campaign_test_key or not goal_identifier:
        return None
    campaign = get_campaign(settings_file, campaign_test_key)
    if not campaign:
        return None
    for goal in campaign.get('goals'):
        if goal.get('identifier') == goal_identifier:
            return goal
    return None


def get_campaign_variation(settings_file, campaign_test_key, variation_name):
    """ Returns variation from given campaign_test_key and variation_name.

    Args:
        settings_file (dict): Settings file of the project
        campaign_test_key (string): Campaign identifier key
        variation_name (string): Variation identifier

    Returns:
        dict: Variation corresponding to variation_name in respective campaign
    """

    if not settings_file or not campaign_test_key or not variation_name:
        return None
    campaign = get_campaign(settings_file, campaign_test_key)
    if not campaign:
        return None
    for variation in campaign.get('variations'):
        if variation.get('name') == variation_name:
            return variation
    return None
