""" Module defining VWO class architecture and exposing API methods """

from .project_config_manager import ProjectConfigManager
from .helpers import impression_util, validate_util
from .event_dispatcher import EventDispatcher
from .helpers import constants, campaign_util
from .helpers.enums import LogMessageEnum, FileNameEnum, LogLevelEnum
from .decision_service import DecisionService
from .logger import Logger

FILE = FileNameEnum.VWO


class VWO(object):
    """ Class encapsulating all SDK functionality. """

    def __init__(self,
                 settings_file,
                 logger=None,
                 user_profile_service=None,
                 is_development_mode=False
                 ):
        """ VWO init method for managing custom projects.
            Setting various services on the instance
            to be accessible by its member functions

        Args:
            settings_file: JSON string representing the project.
            event_dispatcher: Provides a dispatch_event method which
                if given a URL and params sends a request to it.
            logger: Optional component which provides a log method
                to log messages. By default everything would be logged.
            user_profile_service: Optional component which provides
                methods to store and manage user profiles.
            is_development_mode=False: To specify whether the request
                to our server should be sent or not.
        """

        # Verify and assign a/the logger
        self.logger = Logger(logger)

        # Verify the settings_file for json object and correct schema
        if not validate_util.is_valid_settings_file(settings_file):
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.SETTINGS_FILE_CORRUPTED.format(
                    file=FILE
                )
            )
            self.is_valid = False
            return
        self.is_valid = True

        # Initialize the ProjectConfigManager if settings_file provided is valid
        self.config = ProjectConfigManager(settings_file)
        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.VALID_CONFIGURATION.format(
                file=FILE
            )
        )

        # Process the settings file
        self.config.process_settings_file()
        self.settings_file = self.config.get_settings_file()

        # Assign DecisionService to vwo
        self.decision_service = DecisionService(self.settings_file,
                                                user_profile_service
                                                )

        # Assigne event dispatcher
        if is_development_mode:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.SET_DEVELOPMENT_MODE.format(
                    file=FILE
                )
            )
        self.event_dispatcher = EventDispatcher(is_development_mode)

        # Log successfully initiazlized SDK
        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.SDK_INITIALIZED.format(
                file=FILE
            )
        )

    # PUBLIC METHODS

    def activate(self, campaign_test_key, user_id):
        """ This API method: Gets the variation assigned for the user
            for the campaign and send the metrics to VWO server

        1. Validates the arguments being passed
        2. Checks if user is eligible to get bucketed into the campaign,
        3. Assigns the determinitic variation to the user(based on userId),
            if user becomes part of campaign
            If userProfileService is used, it will look into it for the
            variation and if found, no further processing is done
        4. Sends an impression call to VWO server to track user

        Args:
            campaign_test_key (string): unique campaign test key
            user_id (string): ID assigned to a user

        Returns:
            strings|None: If variation is assigned then variation-name
            otherwise None in case of user not becoming part
        """

        # Validate input parameters
        if not validate_util.is_valid_string(campaign_test_key) or not validate_util.is_valid_string(user_id):  # noqa:E501
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.ACTIVATE_API_MISSING_PARAMS.format(  # noqa:E501
                    file=FILE
                )
            )
            return None

        # Validate project config manager
        if not self.is_valid:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.ACTIVATE_API_CONFIG_CORRUPTED.format(  # noqa:E501
                    file=FILE
                )
            )
            return None

        # Get the campaign settings
        campaign = campaign_util.get_campaign(self.settings_file,
                                              campaign_test_key
                                              )

        # Validate campaign
        if not campaign or campaign.get('status') != constants.STATUS_RUNNING:
            # log campaigns invalid
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(
                    file=FILE,
                    campaign_test_key=campaign_test_key,
                    api='activate'
                )
            )
            return None

        # Once the matching RUNNING campaign is found, assign the
        # deterministic variation to the user_id provided
        variation_id, variation_name = self.decision_service.get(user_id,
                                                                 campaign,
                                                                 campaign_test_key  # noqa:E501
                                                                 )

        # Check if variation_name has been assigned
        if not validate_util.is_valid_value(variation_name):
            # log invalid variation key
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.INVALID_VARIATION_KEY.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_test_key=campaign_test_key
                )
            )
            return None

        # Variation found, dispatch log to dacdn
        properties = impression_util.build_event(self.settings_file,
                                                 campaign.get('id'),
                                                 variation_id,
                                                 user_id
                                                 )
        self.event_dispatcher.dispatch(properties)

        return variation_name

    def get_variation(self, campaign_test_key, user_id):
        """ This API method: Gets the variation assigned for the
            user for the campaign

        1. Validates the arguments being passed
        2. Checks if user is eligible to get bucketed into the campaign,
        3. Assigns the determinitic variation to the user(based on userId),
            if user becomes part of campaign
            If userProfileService is used, it will look into it for the
                variation and if found, no further processing is done

        Args:
            campaign_test_key (string): unique campaign test key
            user_id (string): ID assigned to a user

        Returns:
            string|None: If variation is assigned then variation-name
                otherwise null in case of user not becoming part
        """

        # Check for valid arguments
        if not validate_util.is_valid_string(campaign_test_key) or not validate_util.is_valid_string(user_id):  # noqa:E501
            # log invalid params
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.GET_VARIATION_API_MISSING_PARAMS.format(  # noqa:E501
                    file=FILE
                )
            )
            return None

        # Validate project config manager
        if not self.is_valid:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.ACTIVATE_API_CONFIG_CORRUPTED.format(  # noqa:E501
                    file=FILE
                )
            )
            return None

        # Get the campaign settings
        campaign = campaign_util.get_campaign(self.settings_file,
                                              campaign_test_key
                                              )

        # Validate campaign
        if not campaign or campaign.get('status') != constants.STATUS_RUNNING:
            # log campaigns invalid
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(
                    file=FILE,
                    campaign_test_key=campaign_test_key,
                    api='get_variation'
                )
            )
            return None

        variation_id, variation_name = self.decision_service.get(user_id,
                                                                 campaign,
                                                                 campaign_test_key  # noqa:E501
                                                                 )

        # Check if variation_name has been assigned
        if not validate_util.is_valid_value(variation_name):
            # log invalid variation key
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.INVALID_VARIATION_KEY.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_test_key=campaign_test_key
                )
            )
            return None

        return variation_name

    def track(self,
              campaign_test_key,
              user_id,
              goal_identifier,
              *args,
              **kwargs
              ):
        """
        This API method: Marks the conversion of the campaign
        for a particular goal

        1. validates the arguments being passed
        2. Checks if user is eligible to get bucketed into the campaign,
        3. Gets the assigned determinitic variation to the
            user(based on userId), if user becomes part of campaign
        4. Sends an impression call to VWO server to track goal data

        Args:
            campaign_test_key (string): unique campaign test key
            user_id (string): ID assigned to a user
            goal_identifier (string): unique campaign's goal identifier
            revenue_value (int|float|string): revenue generated on
            triggering the goal
        """

        if args:
            revenue_value = args[0]
        elif kwargs:
            revenue_value = kwargs.get('revenue_value', None)
        else:
            revenue_value = None

        # Check for valid args
        if not validate_util.is_valid_string(campaign_test_key) or not validate_util.is_valid_string(user_id) or not validate_util.is_valid_string(goal_identifier):  # noqa:E501
            # log invalid params
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.TRACK_API_MISSING_PARAMS.format(
                    file=FILE
                )
            )
            return False

        if not self.is_valid:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.ACTIVATE_API_CONFIG_CORRUPTED.format(  # noqa:E501
                    file=FILE
                )
            )
            return None

        # Get the campaign settings
        campaign = campaign_util.get_campaign(self.settings_file,
                                              campaign_test_key
                                              )

        # Validate campaign
        if not campaign or campaign.get('status') != constants.STATUS_RUNNING:
            # log error
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(
                    file=FILE,
                    campaign_test_key=campaign_test_key,
                    api='track'
                )
            )
            return False

        campaign_id = campaign.get('id')
        variation_id, variation_name = self.decision_service.get_variation_allotted(user_id, campaign)  # noqa:E501

        if variation_name:
            goal = campaign_util.get_campaign_goal(self.settings_file,
                                                   campaign.get('key'),
                                                   goal_identifier
                                                   )
            if goal:
                properties = impression_util.build_event(self.settings_file,
                                                         campaign_id,
                                                         variation_id,
                                                         user_id,
                                                         goal.get('id'),
                                                         revenue_value
                                                         )
                self.event_dispatcher.dispatch(properties)
                return True
            else:
                # log error
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.TRACK_API_GOAL_NOT_FOUND.format(  # noqa:E501
                        file=FILE,
                        goal=goal_identifier,
                        user_id=user_id,
                        campaign_test_key=campaign_test_key
                    )
                )
                return False
        return False
