""" Utitlity module for manipulating VWO campaigns """

import math
from ..constants import constants
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger.logger_manager import VWOLogger


def get_campaign(settings_file, campaign_key):
    """ Finds and Returns campaign from given campaign_key.

    Args:
        settings_file (dict): Settings file for the project
        campaign_key (string): Campaign identifier key

    Returns:
        dict: Campaign object
    """

    for campaign in settings_file.get('campaigns'):
        if campaign.get('key') == campaign_key:
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
        VWOLogger.getInstance().log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.VARIATION_RANGE_ALLOCATION.format(
                file=FileNameEnum.CampaignUtil,
                campaign_key=campaign.get('key'),
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


def get_campaign_goal(campaign, goal_identifier):
    """ Returns goal from given campaign and Goal_identifier.

    Args:
        campaign (dict): The running campaign
        goal_identifier (string): Goal identifier

    Returns:
        dict: Goal corresponding to goal_identifer in respective campaign
    """

    if not campaign or not goal_identifier:
        return None
    for goal in campaign.get('goals'):
        if goal.get('identifier') == goal_identifier:
            return goal
    return None


def get_campaign_variation(campaign, variation_name):
    """ Returns variation from given campaign and variation_name.

    Args:
        campaign (dict): The running campaign
        variation_name (string): Variation identifier

    Returns:
        dict: Variation corresponding to variation_name in respective campaign
    """

    if not campaign or not variation_name:
        return None
    for variation in campaign.get('variations'):
        if variation.get('name') == variation_name:
            return variation
    return None


def get_variable(variables, variable_key):
    """ Returns variable from given variables list.

    Args:
        variables (list): List of variables, whether in campaigns or
        inside variation
        variable_key (string): Variable identifier

    Returns:
        dict: Variable corresponding to variable_key in given variable list
    """
    for variable in variables:
        if variable.get('key') == variable_key:
            return variable
    return None


def get_control_variation(campaign):
    """ Returns control variation from a given campaing

    Args:
        campaing (dict): Running campaign
    Returns:
        variation (dict): Control variation from the campaign, ie having id = 1
    """

    for variation in campaign.get('variations'):
        if int(variation.get('id')) == 1:
            return variation
    return None
