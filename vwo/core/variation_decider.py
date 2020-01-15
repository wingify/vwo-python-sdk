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

import copy
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..enums.segments.result_status import ResultStatus
from ..helpers import validate_util, campaign_util
from ..logger.logger_manager import VWOLogger
from .bucketer import Bucketer
from ..services.segmentor import SegmentEvaluator
from ..constants import constants

FILE = FileNameEnum.Core.VariationDecider


class VariationDecider(object):
    """ Class responsible for deciding the variation for a visitor """

    def __init__(self, user_storage=None):
        """ Initializes VariationDecider with settings_file,
            UserStorage and logger.

        Args:
            settings_file (dict): settings_file consisting all the campaign
            related data
            user_storage: Class instance having the capability of
                get and set.
        """
        self.logger = VWOLogger.getInstance()
        self.bucketer = Bucketer()
        self.segment_evaluator = SegmentEvaluator()
        # Check if user_storage provided is valid or not
        if validate_util.is_valid_service(user_storage, 'user_storage'):
            self.user_storage = user_storage
        else:
            self.user_storage = None

    def get_variation(self, user_id, campaign, **kwargs):
        """ Returns variation for the user for given campaign
            This method achieves the variation assignment in the following way:
            1. First get variation from UserStorage, if variation is found in user_storage_data,
                return from there
            2. Evaluates white listing users for each variation, and find a targeted variation.
            3. If no targeted variation is found, evaluate pre-segmentation result
            4. Evaluate percent traffic
            5. If user becomes part of campaign assign a variation.
            6. Store the variation found in the user_storage

        Args:
            user_id (string): the unique ID assigned to User
            campaign (dict): campaign in which user is participating
            custom_variables(dict): variables for pre-segmentation, pass it through **kwargs as
            custom_variables = {}
            variation_targeting_variables(dict): variables for variation targeting, pass it through **kwargs as
            variation_targeting_variables = {}

        Returns:
            variation (dict|None): Dict object containing the information regarding variation
            assigned else None
        """

        custom_variables = kwargs.get('custom_variables')
        variation_targeting_variables = kwargs.get('variation_targeting_variables')

        # Evaluate whitelisting at first
        targeted_variation = self.find_targeted_variation(user_id, campaign, variation_targeting_variables)
        if targeted_variation:
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.GOT_VARIATION_FOR_USER.format(
                    file=FILE,
                    variation_name=targeted_variation.get('name'),
                    user_id=user_id,
                    campaign_key=campaign.get('key'),
                    campaign_type=campaign.get('type')
                )
            )
            return targeted_variation

        # Try retrieving data from user_storage
        variation = self.get_variation_from_user_storage(user_id, campaign)
        if variation is not None:
            return variation

        # Evaluate pre-segmentation and percent-traffic
        if self.evaluate_pre_segmentation(user_id, campaign, custom_variables) and \
                self.is_user_part_of_campaign(user_id, campaign):
            variation = self.bucketer.bucket_user_to_variation(user_id, campaign)
            self._set_user_storage_data(user_id, campaign.get('key'), variation.get('name'))
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.GOT_VARIATION_FOR_USER.format(
                    file=FILE,
                    variation_name=variation.get('name'),
                    user_id=user_id,
                    campaign_key=campaign.get('key'),
                    campaign_type=campaign.get('type')
                )
            )
            return variation

        # No variation
        self.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.USER_GOT_NO_VARIATION.format(
                file=FILE,
                user_id=user_id,
                campaign_key=campaign.get('key'),
                campaign_type=campaign.get('type')
            )
        )
        return None

    def get_variation_from_user_storage(self, user_id, campaign):
        """ Tries retrieving variation from user_storage

        Args:
            user_id(string): unique user identifier
            campaign(dict): campaign for which the variation is to be retrieved

        Returns:
            variation (dict|None): Dict object containing the information regarding variation
            assigned else None
        """

        user_storage_data = self._get_user_storage_data(user_id, campaign.get('key'))
        if validate_util.is_valid_dict(user_storage_data):
            variation = self._get_stored_variation(user_id,
                                                   campaign,
                                                   user_storage_data)
            if variation:
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.GOT_STORED_VARIATION.format(
                        file=FILE,
                        campaign_key=campaign.get('key'),
                        user_id=user_id,
                        variation_name=variation.get('name')
                    )
                )
                return variation
        return None

    def find_targeted_variation(self, user_id, campaign, variation_targeting_variables):
        """ Identifies and retrives if there exists any targeted variation in the given campaign
        for given user_id

        Args:
            user_id(string): unique user identifier
            campaign(dict): campaign for which the variation is to be retrieved
            variation_targeting_variables(dict): variables for finding targeted variation

        Returns:
            targeted_variation (dict|None): Dict object containing the information regarding forced
            variation assigned else None
        """
        if campaign.get('isForcedVariationEnabled') is not True:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.WHITELISTING_SKIPPED.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_key=campaign.get('key'),
                )
            )
            return None
        else:
            white_listed_variations_list = self._get_white_listed_variations_list(user_id,
                                                                                  campaign,
                                                                                  variation_targeting_variables)
            white_listed_variations_len = len(white_listed_variations_list)
            if white_listed_variations_len == 0:
                targeted_variation = None
            elif white_listed_variations_len == 1:
                targeted_variation = white_listed_variations_list[0]
            else:
                # Scale the traffic percent of each variation
                campaign_util.scale_variations(white_listed_variations_list)
                # Allocate new range
                variation_allocations = campaign_util.get_variation_allocation_ranges(white_listed_variations_list)
                campaign_util.set_variation_allocation_from_ranges(white_listed_variations_list, variation_allocations)
                # Now retrieve the variation from the modified_campaign_for_whitelisting
                bucket_value = self.bucketer.get_bucket_value_for_user(user_id, constants.MAX_TRAFFIC_VALUE)
                targeted_variation = self.bucketer.get_variation(white_listed_variations_list, bucket_value)
            variation_status = 'and variation {variation_name} is assigned'
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.SEGMENTATION_STATUS.format(
                    file=FILE,
                    campaign_key=campaign.get('key'),
                    user_id=user_id,
                    variables=variation_targeting_variables,
                    variation_status=variation_status.format(variation_name=targeted_variation.get('name')
                                                             if targeted_variation else None),
                    segmentation_type='whitelisting',
                    status=ResultStatus.PASSED if targeted_variation is not None else ResultStatus.FAILED
                )
            )
            return targeted_variation

    def evaluate_pre_segmentation(self, user_id, campaign, custom_variables):
        """ Evaluates segmentation for the user_id against the segments found inside
        the campaign.

        Args:
            user_id(string): unique user identifier
            campaign(dict): running campaign for which the segments is to be evaluated
            custom_variables(dict): variables for segmentation

        Returns:
            bool: True if user passes segmentation, else False
        """
        segments = campaign.get('segments')
        if not validate_util.is_valid_value(segments):
            result = True
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.SEGMENTATION_SKIPPED.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_key=campaign.get('key'),
                    variables=custom_variables,
                    variation_status=''
                )
            )
        else:
            if not validate_util.is_valid_value(custom_variables):
                self.logger.log(
                    LogLevelEnum.DEBUG,
                    LogMessageEnum.DEBUG_MESSAGES.NO_VARIABLES.format(
                        file=FILE,
                        user_id=user_id,
                        campaign_key=campaign.get('key'),
                        segmentation_type='pre_segmentation'
                    )
                )
                custom_variables = {}
            try:
                result = self.segment_evaluator.evaluate(segments, custom_variables)
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.SEGMENTATION_STATUS.format(
                        file=FILE,
                        user_id=user_id,
                        campaign_key=campaign.get('key'),
                        variables=custom_variables,
                        variation_status='',
                        segmentation_type='pre_segmentation',
                        status=ResultStatus.PASSED if result else ResultStatus.FAILED
                    )
                )
            except Exception as e:
                result = False
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.SEGMENTATION_ERROR.format(
                        file=FILE,
                        user_id=user_id,
                        campaign_key=campaign.get('key'),
                        variables=custom_variables,
                        variation_status='',
                        error_message=e,
                    )
                )
        return result

    def is_user_part_of_campaign(self, user_id, campaign):
        """ Evaluates whether the user should become part of campaign
        or not

        Args:
            user_id (string): the unique ID assigned to User
            campaign (dict): campaign in which user is participating

        Returns:
            bool: True if user should become part of campaign, else False
        """

        if self.bucketer.is_user_part_of_campaign(user_id, campaign):
           return True
        else:
            # not part of campaign
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.USER_NOT_PART_OF_CAMPAIGN.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_key=campaign.get('key'),
                    method='is_user_part_of_campaign',
                    campaign_type=campaign.get('type')
                )
            )
            return False

    # Private helper methods

    def _get_white_listed_variations_list(self, user_id, campaign, variation_targeting_variables):
        """ Identifies all forced variations which are targeted by variation_targeting_variables

        Args:
            user_id(string): unique user identifier
            campaign(dict): campaign for which the targeted variation(s) is to be retrieved
            variation_targeting_variables(dict): variables for variation targeting

        Returns:
            targeted_variation (list): List of targeted variation objects
        """
        if not validate_util.is_valid_value(variation_targeting_variables):
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.NO_VARIABLES.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_key=campaign.get('key'),
                    segmentation_type='whitelisting'
                )
            )
            variation_targeting_variables = {}

        variation_targeting_variables.update(_vwo_user_id=user_id)
        white_listed_variations_list = []

        for variation in campaign.get('variations'):
            if not validate_util.is_valid_value(variation.get('segments')):
                result = False
                self.logger.log(
                    LogLevelEnum.DEBUG,
                    LogMessageEnum.DEBUG_MESSAGES.SEGMENTATION_SKIPPED.format(
                        file=FILE,
                        user_id=user_id,
                        variation_name=variation.get('name'),
                        campaign_key=campaign.get('key'),
                        variation_status='for variation %s' % variation.get('name')
                    )
                )
            else:
                try:
                    result = self.segment_evaluator.evaluate(variation.get('segments'), variation_targeting_variables)
                    self.logger.log(
                        LogLevelEnum.DEBUG,
                        LogMessageEnum.DEBUG_MESSAGES.SEGMENTATION_STATUS.format(
                            file=FILE,
                            user_id=user_id,
                            status='passed' if result else 'failed',
                            variables=variation_targeting_variables,
                            variation_status='for variation %s' % variation.get('name'),
                            campaign_key=campaign.get('key'),
                            segmentation_type='white_listing'
                        )
                    )
                except Exception as e:
                    result = False
                    self.logger.log(
                        LogLevelEnum.ERROR,
                        LogMessageEnum.ERROR_MESSAGES.SEGMENTATION_ERROR.format(
                            file=FILE,
                            user_id=user_id,
                            variables=variation_targeting_variables,
                            campaign_key=campaign.get('key'),
                            variation_status=' for variation %s' % variation.get('name'),
                            error_message=e,
                        )
                    )
            if result:
                white_listed_variations_list.append(variation)
        return white_listed_variations_list

    def _get_stored_variation(self, user_id, campaign, user_storage_data):
        """ If UserStorage is provided and variation was stored,
        get the stored variation

        Args:
            user_id (string): Unique user identifier
            campaign_key (string): Unique campaign identifier
            user_storage_data (dict):
                CampaignMap consisting the stored user variation

        Returns:
            (Object|None): if found then variation object
                otherwise None
        """

        if user_storage_data.get('campaignKey') == campaign.get('key'):
            variation_name = user_storage_data.get('variationName')
            if validate_util.is_valid_string(variation_name):
                self.logger.log(
                    LogLevelEnum.DEBUG,
                    LogMessageEnum.DEBUG_MESSAGES.GETTING_STORED_VARIATION.format(
                        file=FILE,
                        campaign_key=campaign.get('key'),
                        user_id=user_id,
                        variation_name=variation_name
                    )
                )
                return campaign_util.get_campaign_variation(campaign, variation_name)

        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.NO_STORED_VARIATION.format(
                file=FILE,
                campaign_key=campaign.get('key'),
                user_id=user_id
            )
        )
        return None

    def _get_user_storage_data(self, user_id, campaign_key):
        """ Get the UserStorageData after looking up into get method
        being provided via UserStorage service

        Args:
            user_id (string): Unique user identifier
            campaign_key (string): Unique campaign identifier
        Returns:
            dict: user_storage_data data
        """

        if not self.user_storage:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.NO_USER_STORAGE_GET.format(
                    file=FILE
                )
            )
            return False
        try:
            user_storage_data = self.user_storage.get(user_id, campaign_key)
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.LOOKING_UP_USER_STORAGE.format(
                    file=FILE,
                    user_id=user_id
                )
            )
            return copy.deepcopy(user_storage_data)
        except Exception:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.LOOK_UP_USER_STORAGE_FAILED.format(
                    file=FILE,
                    user_id=user_id
                )
            )
            return False

    def _set_user_storage_data(self, user_id, campaign_key, variation_name):
        """ If UserStorage is provided and variation was found,
        set the assigned variation in UserStorage.
            It creates bucket and then stores.

        Args:
            user_id (string): Unique user identifier
            campaign_key (string): Unique campaign identifier
            variation_name (string): variation identifier

        Returns:
            bool: true if found otherwise false
        """

        if not self.user_storage:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.NO_USER_STORAGE_SET.format(
                    file=FILE
                )
            )
            return False

        new_user_storage_data = {
            "userId": user_id,
            "campaignKey": campaign_key,
            "variationName": variation_name
        }
        try:
            status = self.user_storage.set(new_user_storage_data)
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.SAVING_DATA_USER_STORAGE_STATUS.format(
                    file=FILE,
                    user_id=user_id,
                    status='successful' if status else 'failed'
                )
            )
            return status
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.SET_USER_STORAGE_FAILED.format(
                    file=FILE,
                    user_id=user_id,
                    error_message=e
                )
            )
            return False
