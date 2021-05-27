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

import copy
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..enums.hooks_enum import HooksEnum
from ..enums.segments.result_status import ResultStatus
from ..helpers import validate_util, campaign_util, uuid_util
from ..logger import VWOLogger
from .bucketer import Bucketer
from ..services.segmentor import SegmentEvaluator
from ..services.hooks_manager import HooksManager
from ..constants import constants

FILE = FileNameEnum.Core.VariationDecider


class VariationDecider(object):
    """ Class responsible for deciding the variation for a visitor """

    def __init__(self, user_storage=None, account_id=None, integrations=None):
        """Initializes VariationDecider with settings_file,
            UserStorage and logger.

        Args:
            user_storage (Class|None): Class instance having the capability of
                get and set.
            account_id (string): Account ID of user
            integrations (dict|None): an integrations service instance for third party integrations
        """
        self.logger = VWOLogger.getInstance()
        self.bucketer = Bucketer()
        self.segment_evaluator = SegmentEvaluator()
        self.user_storage = user_storage
        self.account_id = account_id
        self.hooks_manager = HooksManager(integrations) if integrations else None

    def get_variation(self, user_id, campaign, **kwargs):
        """Returns variation for the user for given campaign
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
            api_method (string): api's name calling get_variation method

        Returns:
            variation (dict|None): Dict object containing the information regarding variation
            assigned else None
        """

        custom_variables = kwargs.get("custom_variables")
        variation_targeting_variables = kwargs.get("variation_targeting_variables")
        goal_data = kwargs.get("goal_data")
        api_method = kwargs.get("api_method")

        decision = {
            # campaign info
            "campaign_id": campaign.get("id"),
            "campaign_name": campaign.get("name"),
            "campaign_key": campaign.get("key"),
            "campaign_type": campaign.get("type"),
            # campaign segmentation conditions
            "custom_variables": custom_variables,
            # event name
            "event": HooksEnum.DecisionTypes.CAMPAIGN_DECISION,
            # goal tracked in case of track API
            "goal_identifier": goal_data and goal_data.get("identifier"),
            # campaign whitelisting flag
            "is_forced_variation_enabled": campaign.get("isForcedVariationEnabled"),
            "sdk_version": constants.SDK_VERSION,
            # API name which triggered the event
            "source": api_method,
            # Passed in API
            "user_id": user_id,
            # Campaign Whitelisting conditions
            "variation_targeting_variables": variation_targeting_variables,
            # VWO generated UUID based on passed UserId and Account ID
            "vwo_user_id": uuid_util.generate_for(user_id, self.account_id),
        }

        # Evaluate whitelisting at first
        targeted_variation = self.find_targeted_variation(user_id, campaign, variation_targeting_variables)
        if targeted_variation:
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.GOT_VARIATION_FOR_USER.format(
                    file=FILE,
                    variation_name=targeted_variation.get("name"),
                    user_id=user_id,
                    campaign_key=campaign.get("key"),
                    campaign_type=campaign.get("type"),
                ),
            )

            decision.update({"from_user_storage_service": False, "is_user_whitelisted": True})
            if campaign.get("type") == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
                decision.update({"is_feature_enabled": True})
            else:
                if campaign.get("type") == constants.CAMPAIGN_TYPES.FEATURE_TEST:
                    decision.update({"is_feature_enabled": targeted_variation.get("isFeatureEnabled")})

                decision.update(
                    {"variation_id": targeted_variation.get("id"), "variation_name": targeted_variation.get("name")}
                )
            if self.hooks_manager is not None:
                self.hooks_manager.execute(decision)

            return targeted_variation

        campaign_type = campaign.get("type")
        is_user_tracked = self.identify_tracked_user_from_user_storage(user_id, campaign_key=campaign.get("key"))
        if (
            bool(self.user_storage) is True
            and is_user_tracked is False
            and campaign_type != constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT
            and api_method not in [constants.API_METHODS.IS_FEATURE_ENABLED, constants.API_METHODS.ACTIVATE, None]
        ):

            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.CAMPAIGN_NOT_ACTIVATED.format(
                    file=FILE, campaign_key=campaign.get("key"), user_id=user_id, api_method=api_method
                ),
            )

            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.CAMPAIGN_NOT_ACTIVATED.format(
                    file=FILE,
                    campaign_key=campaign.get("key"),
                    user_id=user_id,
                    reason="track it" if api_method is constants.API_METHODS.TRACK else "get the decision/value",
                ),
            )

            return None

        # Try retrieving data from user_storage
        user_storage_data = self._get_user_storage_data(user_id, campaign.get("key"))
        if user_storage_data:
            # If being called by track, check for goals identified
            if goal_data:
                is_goal_tracked = self.identify_tracked_goal_from_user_storage(goal_data, user_storage_data)
                if is_goal_tracked:
                    self.logger.log(
                        LogLevelEnum.INFO,
                        LogMessageEnum.INFO_MESSAGES.GOAL_ALREADY_TRACKED.format(
                            file=FILE,
                            goal_identifier=goal_data.get("identifier"),
                            campaign_key=campaign.get("key"),
                            user_id=user_id,
                        ),
                    )
                    return None
            # Retreving variation from user_storage_data
            variation = self.get_variation_from_user_storage(user_id, campaign, user_storage_data)
            # Setting goal information if variation found and api is track
            if variation is not None:
                if goal_data:
                    self.update_goals_tracked_in_user_storage(goal_data, user_storage_data)

                decision.update({"from_user_storage_service": True, "is_user_whitelisted": False})
                if campaign.get("type") == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
                    decision.update({"is_feature_enabled": True})
                else:
                    if campaign.get("type") == constants.CAMPAIGN_TYPES.FEATURE_TEST:
                        decision.update({"is_feature_enabled": variation.get("isFeatureEnabled")})

                    decision.update({"variation_id": variation.get("id"), "variation_name": variation.get("name")})

                if self.hooks_manager is not None:
                    self.hooks_manager.execute(decision)

                return variation

        # Evaluate pre-segmentation and percent-traffic
        if self.evaluate_pre_segmentation(user_id, campaign, custom_variables) and self.is_user_part_of_campaign(
            user_id, campaign
        ):
            variation = self.bucketer.bucket_user_to_variation(user_id, campaign)
            new_user_storage_data = self._create_user_storage_data(
                user_id, campaign.get("key"), variation.get("name"), goal_data=kwargs.get("goal_data")
            )
            self._set_user_storage_data(new_user_storage_data)
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.GOT_VARIATION_FOR_USER.format(
                    file=FILE,
                    variation_name=variation.get("name"),
                    user_id=user_id,
                    campaign_key=campaign.get("key"),
                    campaign_type=campaign.get("type"),
                ),
            )

            decision.update({"from_user_storage_service": False, "is_user_whitelisted": False})
            if campaign.get("type") == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
                decision.update({"is_feature_enabled": True})
            else:
                if campaign.get("type") == constants.CAMPAIGN_TYPES.FEATURE_TEST:
                    decision.update({"is_feature_enabled": variation.get("isFeatureEnabled")})

                decision.update({"variation_id": variation.get("id"), "variation_name": variation.get("name")})

            if self.hooks_manager is not None:
                self.hooks_manager.execute(decision)

            return variation

        # No variation
        self.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.USER_GOT_NO_VARIATION.format(
                file=FILE, user_id=user_id, campaign_key=campaign.get("key"), campaign_type=campaign.get("type")
            ),
        )
        return None

    def identify_tracked_goal_from_user_storage(self, goal_data, user_storage_data):
        """Identifies whether the given goal has been already tracked or not.

        Args:
            goal_data (dict): goal related data
            user_storage_data (dict): data retrieved from user_storage

        Returns:
            bool: True if goal already tracked else False
        """
        goals_tracked = user_storage_data.get("goalIdentifiers")
        if (
            goals_tracked
            and (goal_data.get("identifier") in goals_tracked.split("_vwo_"))
            and not goal_data.get("should_track_returning_user")
        ):
            return True
        return False

    def identify_tracked_user_from_user_storage(self, user_id, campaign_key):
        """Identifies whether a user has been already tracked or not.

        Args:
            user_id (string): the unique ID assigned to User
            campaign_key (string): Unique campaign identifier

        Returns:
            bool: True if user has already been tracked else False
        """
        user_storage_data = self._get_user_storage_data(user_id, campaign_key)
        return bool(user_storage_data)

    def update_goals_tracked_in_user_storage(self, goal_data, user_storage_data):
        """Updates the goals tracked information stored inside the user_storage service

        Args:
            goal_data (dict): the goal related data
            user_storage_data (dict): new or retrieved user_storage_data
        """
        goals_tracked = user_storage_data.get("goalIdentifiers")
        if goals_tracked:
            updated_goals_tracked = goals_tracked + "_vwo_" + goal_data.get("identifier")
        else:
            updated_goals_tracked = goal_data.get("identifier")
        user_storage_data["goalIdentifiers"] = updated_goals_tracked
        self._set_user_storage_data(user_storage_data)

    def get_variation_from_user_storage(self, user_id, campaign, user_storage_data):
        """Tries retrieving variation from user_storage

        Args:
            user_id(string): unique user identifier
            campaign(dict): campaign for which the variation is to be retrieved

        Returns:
            variation (dict|None): Dict object containing the information regarding variation
            assigned else None
        """
        if validate_util.is_valid_dict(user_storage_data):
            if user_storage_data.get("campaignKey") == campaign.get("key"):
                variation_name = user_storage_data.get("variationName")
                if validate_util.is_valid_string(variation_name):
                    variation = campaign_util.get_campaign_variation(campaign, variation_name)
                    if variation:
                        self.logger.log(
                            LogLevelEnum.INFO,
                            LogMessageEnum.INFO_MESSAGES.GOT_STORED_VARIATION.format(
                                file=FILE,
                                campaign_key=campaign.get("key"),
                                user_id=user_id,
                                variation_name=variation.get("name"),
                            ),
                        )
                        return variation
        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.NO_STORED_VARIATION.format(
                file=FILE, campaign_key=campaign.get("key"), user_id=user_id
            ),
        )
        return None

    def find_targeted_variation(self, user_id, campaign, variation_targeting_variables):
        """Identifies and retrives if there exists any targeted variation in the given campaign
        for given user_id

        Args:
            user_id(string): unique user identifier
            campaign(dict): campaign for which the variation is to be retrieved
            variation_targeting_variables(dict): variables for finding targeted variation

        Returns:
            targeted_variation (dict|None): Dict object containing the information regarding forced
            variation assigned else None
        """
        if campaign.get("isForcedVariationEnabled") is not True:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.WHITELISTING_SKIPPED.format(
                    file=FILE, user_id=user_id, campaign_key=campaign.get("key")
                ),
            )
            return None
        else:
            white_listed_variations_list = self._get_white_listed_variations_list(
                user_id, campaign, variation_targeting_variables
            )
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
            variation_status = "and variation {variation_name} is assigned"
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.SEGMENTATION_STATUS.format(
                    file=FILE,
                    campaign_key=campaign.get("key"),
                    user_id=user_id,
                    variables=variation_targeting_variables,
                    variation_status=variation_status.format(
                        variation_name=targeted_variation.get("name") if targeted_variation else None
                    ),
                    segmentation_type="whitelisting",
                    status=ResultStatus.PASSED if targeted_variation is not None else ResultStatus.FAILED,
                ),
            )
            return targeted_variation

    def evaluate_pre_segmentation(self, user_id, campaign, custom_variables):
        """Evaluates segmentation for the user_id against the segments found inside
        the campaign.

        Args:
            user_id(string): unique user identifier
            campaign(dict): running campaign for which the segments is to be evaluated
            custom_variables(dict): variables for segmentation

        Returns:
            bool: True if user passes segmentation, else False
        """
        segments = campaign.get("segments")
        if not validate_util.is_valid_value(segments):
            result = True
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.SEGMENTATION_SKIPPED.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_key=campaign.get("key"),
                    variables=custom_variables,
                    variation_status="",
                ),
            )
        else:
            if not validate_util.is_valid_value(custom_variables):
                self.logger.log(
                    LogLevelEnum.DEBUG,
                    LogMessageEnum.DEBUG_MESSAGES.NO_VARIABLES.format(
                        file=FILE,
                        user_id=user_id,
                        campaign_key=campaign.get("key"),
                        segmentation_type="pre_segmentation",
                    ),
                )
                custom_variables = {}
            try:
                result = self.segment_evaluator.evaluate(segments, custom_variables)
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.SEGMENTATION_STATUS.format(
                        file=FILE,
                        user_id=user_id,
                        campaign_key=campaign.get("key"),
                        variables=custom_variables,
                        variation_status="",
                        segmentation_type="pre_segmentation",
                        status=ResultStatus.PASSED if result else ResultStatus.FAILED,
                    ),
                )
            except Exception as e:
                result = False
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.SEGMENTATION_ERROR.format(
                        file=FILE,
                        user_id=user_id,
                        campaign_key=campaign.get("key"),
                        variables=custom_variables,
                        variation_status="",
                        error_message=e,
                    ),
                )
        return result

    def is_user_part_of_campaign(self, user_id, campaign):
        """Evaluates whether the user should become part of campaign
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
                    campaign_key=campaign.get("key"),
                    method="is_user_part_of_campaign",
                    campaign_type=campaign.get("type"),
                ),
            )
            return False

    # Private helper methods

    def _get_white_listed_variations_list(self, user_id, campaign, variation_targeting_variables):
        """Identifies all forced variations which are targeted by variation_targeting_variables

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
                    file=FILE, user_id=user_id, campaign_key=campaign.get("key"), segmentation_type="whitelisting"
                ),
            )
            variation_targeting_variables = {}

        variation_targeting_variables.update(_vwo_user_id=user_id)
        white_listed_variations_list = []

        for variation in campaign.get("variations"):
            if not validate_util.is_valid_value(variation.get("segments")):
                result = False
                self.logger.log(
                    LogLevelEnum.DEBUG,
                    LogMessageEnum.DEBUG_MESSAGES.SEGMENTATION_SKIPPED.format(
                        file=FILE,
                        user_id=user_id,
                        variation_name=variation.get("name"),
                        campaign_key=campaign.get("key"),
                        variation_status="for variation %s" % variation.get("name"),
                    ),
                )
            else:
                try:
                    result = self.segment_evaluator.evaluate(variation.get("segments"), variation_targeting_variables)
                    self.logger.log(
                        LogLevelEnum.DEBUG,
                        LogMessageEnum.DEBUG_MESSAGES.SEGMENTATION_STATUS.format(
                            file=FILE,
                            user_id=user_id,
                            status="passed" if result else "failed",
                            variables=variation_targeting_variables,
                            variation_status="for variation %s" % variation.get("name"),
                            campaign_key=campaign.get("key"),
                            segmentation_type="white_listing",
                        ),
                    )
                except Exception as e:
                    result = False
                    self.logger.log(
                        LogLevelEnum.ERROR,
                        LogMessageEnum.ERROR_MESSAGES.SEGMENTATION_ERROR.format(
                            file=FILE,
                            user_id=user_id,
                            variables=variation_targeting_variables,
                            campaign_key=campaign.get("key"),
                            variation_status=" for variation %s" % variation.get("name"),
                            error_message=e,
                        ),
                    )
            if result:
                white_listed_variations_list.append(copy.deepcopy(variation))
        return white_listed_variations_list

    def _create_user_storage_data(self, user_id, campaign_key, variation_name, **kwargs):
        """Creates a user_storage_data object to be set by user_storage service implemented by user

        Args:
            user_id (str): unique user ID
            campaign_key (str): campaign key
            variation_name (str): winner of the campaign

        Keyword Args:
            goal_data (dict): goal related data if track api being called

        Returns:
            dict: a user_storage_data object with specified properties
        """
        new_user_storage_data = {"userId": user_id, "campaignKey": campaign_key, "variationName": variation_name}
        # For track only, to store the goals tracked
        if kwargs.get("goal_data"):
            new_user_storage_data["goalIdentifiers"] = kwargs.get("goal_data").get("identifier")
        return new_user_storage_data

    def _get_user_storage_data(self, user_id, campaign_key):
        """Get the UserStorageData after looking up into get method
        being provided via UserStorage service

        Args:
            user_id (string): Unique user identifier
            campaign_key (string): Unique campaign identifier
        Returns:
            dict: user_storage_data data
        """

        if not self.user_storage:
            self.logger.log(LogLevelEnum.DEBUG, LogMessageEnum.DEBUG_MESSAGES.NO_USER_STORAGE_GET.format(file=FILE))
            return False
        try:
            user_storage_data = self.user_storage.get(user_id, campaign_key)
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.LOOKING_UP_USER_STORAGE.format(file=FILE, user_id=user_id),
            )
            return copy.deepcopy(user_storage_data)
        except Exception:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.LOOK_UP_USER_STORAGE_FAILED.format(file=FILE, user_id=user_id),
            )
            return False

    def _set_user_storage_data(self, user_storage_data):
        """If UserStorage is provided and variation was found,
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
            self.logger.log(LogLevelEnum.DEBUG, LogMessageEnum.DEBUG_MESSAGES.NO_USER_STORAGE_SET.format(file=FILE))
            return False

        try:
            self.user_storage.set(user_storage_data)
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.SAVING_DATA_USER_STORAGE_STATUS.format(
                    file=FILE, user_id=user_storage_data.get("userId"), status="successful"
                ),
            )
            return True
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.SET_USER_STORAGE_FAILED.format(
                    file=FILE, user_id=user_storage_data.get("userId"), error_message=e
                ),
            )
            return False
