from .services.settings_file_manager import SettingsFileManager
from .event.event_dispatcher import EventDispatcher
from .helpers import impression_util
from .constants import constants
from .helpers import campaign_util, validate_util, feature_util
from .enums.log_message_enum import LogMessageEnum
from .enums.file_name_enum import FileNameEnum
from .enums.log_level_enum import LogLevelEnum
from .core.variation_decider import VariationDecider
from .logger.logger_manager import VWOLogger, configure_logger

FILE = FileNameEnum.VWO


class VWO(object):
    """ The VWO class which exposes all the SDK APIs for full stack
    server side optimization. """

    def __init__(self,
                 settings_file,
                 logger=None,
                 user_storage=None,
                 is_development_mode=False,
                 *args,
                 **kwargs):
        """ Initializes the services required by the VWO APIs.

        Args:
            settings_file: JSON string representing the project.
            logger(object): Optional component which provides a log method
                to log messages. By default everything would be logged.
            user_storage(object): Optional component which provides
                methods to store and manage user data.
            is_development_mode(bool): To specify whether the request
                to our server should be sent or not.
        """

        # Retrieve log level from args/kwargs
        if not logger:
            log_level = None
            if kwargs:
                log_level = kwargs.get('log_level', None)
            self.logger = VWOLogger.getInstance(configure_logger(level=log_level))
        else:
            # Verify and assign a/the logger
            self.logger = VWOLogger.getInstance(logger)

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

        # Initialize the SettingsFileManager if settings_file provided is valid
        self.config = SettingsFileManager(settings_file)
        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.VALID_CONFIGURATION.format(
                file=FILE
            )
        )

        # Process the settings file
        self.config.process_settings_file()
        self.settings_file = self.config.get_settings_file()

        # Assign VariationDecider to vwo
        self.variation_decider = VariationDecider(self.settings_file,
                                                  user_storage
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

    def activate(self, campaign_key, user_id):
        """ This API method: Gets the variation assigned for the user
            for the campaign and send the metrics to VWO server

        1. Validates the arguments being passed
        2. Checks if user is eligible to get bucketed into the campaign,
        3. Assigns the determinitic variation to the user(based on userId),
            if user becomes part of campaign
            If UserStorage is used, it will look into it for the
            variation and if found, no further processing is done
        4. Sends an impression call to VWO server to track user

        Args:
            campaign_key (string): unique campaign test key
            user_id (string): ID assigned to a user

        Returns:
            strings|None: If variation is assigned then variation-name
            otherwise None in case of user not becoming part
        """

        try:
            # Validate input parameters
            if not validate_util.is_valid_string(campaign_key) or not validate_util.is_valid_string(user_id):
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.ACTIVATE_API_MISSING_PARAMS.format(
                        file=FILE
                    )
                )
                return None

            # Validate project config manager
            if not self.is_valid:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.ACTIVATE_API_CONFIG_CORRUPTED.format(
                        file=FILE
                    )
                )
                return None

            # Get the campaign settings
            campaign = campaign_util.get_campaign(self.settings_file,
                                                  campaign_key)

            # Validate campaign
            if not campaign or campaign.get('status') != constants.STATUS_RUNNING:
                # log campaigns invalid
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(
                        file=FILE,
                        campaign_key=campaign_key,
                        api_name='activate'
                    )
                )
                return None

            # Get campaing type
            campaign_type = campaign.get('type')

            # Validate valid api call
            if campaign_type != constants.CAMPAIGN_TYPES.VISUAL_AB:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                        file=FILE,
                        api_name='activate',
                        user_id=user_id,
                        campaign_key=campaign_key,
                        campaign_type=campaign_type
                    )
                )
                return None

            # Once the matching RUNNING campaign is found, assign the
            # deterministic variation to the user_id provided
            variation = self.variation_decider.get_variation(user_id,
                                                             campaign,
                                                             campaign_key
                                                             )

            # Check if variation_name has been assigned
            if not variation:
                return None

            # Variation found, dispatch log to dacdn
            impression = impression_util.create_impression(self.settings_file,
                                                           campaign.get('id'),
                                                           variation.get('id'),
                                                           user_id)
            self.event_dispatcher.dispatch(impression)

            return variation.get('name')
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    api_name='activate',
                    exception=e
                )
            )

    def get_variation_name(self, campaign_key, user_id):
        """ This API method: Gets the variation name assigned for the
            user for the campaign

        1. Validates the arguments being passed
        2. Checks if user is eligible to get bucketed into the campaign,
        3. Assigns the determinitic variation to the user(based on userId),
            if user becomes part of campaign
            If UserStorage is used, it will look into it for the
                variation and if found, no further processing is done

        Args:
            campaign_key (string): unique campaign test key
            user_id (string): ID assigned to a user

        Returns:
            string|None: If variation is assigned then variation-name
                otherwise null in case of user not becoming part
        """

        try:
            # Check for valid arguments
            if not validate_util.is_valid_string(campaign_key) or not validate_util.is_valid_string(user_id):
                # log invalid params
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.GET_VARIATION_NAME_API_MISSING_PARAMS.format(
                        file=FILE
                    )
                )
                return None

            # Validate project config manager
            if not self.is_valid:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.ACTIVATE_API_CONFIG_CORRUPTED.format(
                        file=FILE
                    )
                )
                return None

            # Get the campaign settings
            campaign = campaign_util.get_campaign(self.settings_file,
                                                  campaign_key)

            # Validate campaign
            if not campaign or campaign.get('status') != constants.STATUS_RUNNING:
                # log campaigns invalid
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(
                        file=FILE,
                        campaign_key=campaign_key,
                        api_name='get_variation_name'
                    )
                )
                return None

            campaign_type = campaign.get('type')

            if campaign_type == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                        file=FILE,
                        api_name='get_variation_name',
                        user_id=user_id,
                        campaign_key=campaign_key,
                        campaign_type=campaign_type
                    )
                )
                return None

            variation = self.variation_decider.get_variation(user_id,
                                                             campaign,
                                                             campaign_key
                                                             )

            # Check if variation_name has been assigned
            if not variation:
                return None

            return variation.get('name')
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    api_name='get_variation_name',
                    exception=e
                )
            )

    def track(self,
              campaign_key,
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
            campaign_key (string): unique campaign test key
            user_id (string): ID assigned to a user
            goal_identifier (string): unique campaign's goal identifier
            revenue_value (int|float|string): revenue generated on
            triggering the goal
        """

        try:
            # Add check for campaign_type
            if args:
                revenue_value = args[0]
            elif kwargs:
                revenue_value = kwargs.get('revenue_value', None)
            else:
                revenue_value = None

            # Check for valid args
            if not validate_util.is_valid_string(campaign_key) \
                or not validate_util.is_valid_string(user_id) \
                    or not validate_util.is_valid_string(goal_identifier):
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
                    LogMessageEnum.ERROR_MESSAGES.ACTIVATE_API_CONFIG_CORRUPTED.format(
                        file=FILE
                    )
                )
                return False

            # Get the campaign settings
            campaign = campaign_util.get_campaign(self.settings_file,
                                                  campaign_key)

            # Validate campaign
            if not campaign or campaign.get('status') != constants.STATUS_RUNNING:
                # log error
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(
                        file=FILE,
                        campaign_key=campaign_key,
                        api_name='track'
                    )
                )
                return False

            campaign_type = campaign.get('type')

            if campaign_type == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                        file=FILE,
                        api_name='track',
                        user_id=user_id,
                        campaign_key=campaign_key,
                        campaign_type=campaign_type
                    )
                )
                return False

            campaign_id = campaign.get('id')
            variation = self.variation_decider.get_variation_allotted(user_id,
                                                                      campaign)

            if variation:
                goal = campaign_util.get_campaign_goal(campaign,
                                                       goal_identifier)
                if not goal:
                    self.logger.log(
                        LogLevelEnum.ERROR,
                        LogMessageEnum.ERROR_MESSAGES.TRACK_API_GOAL_NOT_FOUND.format(
                            file=FILE,
                            goal_identifier=goal_identifier,
                            user_id=user_id,
                            campaign_key=campaign_key
                        )
                    )
                    return False
                elif goal.get('type') == constants.GOAL_TYPES.REVENUE and \
                        not validate_util.is_valid_value(revenue_value):
                    self.logger.log(
                        LogLevelEnum.ERROR,
                        LogMessageEnum.ERROR_MESSAGES.TRACK_API_REVENUE_NOT_PASSED_FOR_REVENUE_GOAL.format(
                            file=FILE,
                            user_id=user_id,
                            goal_identifier=goal_identifier,
                            campaign_key=campaign_key
                        )
                    )
                    return False

                if goal.get('type') == constants.GOAL_TYPES.CUSTOM:
                    revenue_value = None

                impression = impression_util.create_impression(self.settings_file,
                                                               campaign_id,
                                                               variation.get('id'),
                                                               user_id,
                                                               goal.get('id'),
                                                               revenue_value)
                self.event_dispatcher.dispatch(impression)
                return True
            return False
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    api_name='track',
                    exception=e
                )
            )

    def is_feature_enabled(self, campaign_key, user_id):
        """ This API method: Identifies whether the user becomes a part
        of feature rollout/test or not.

        1. Validates the arguments being passed
        2. Checks if user is eligible to get bucketed into the
            feature test/rollout,
        3. Assigns the determinitic variation to the user(based on userId),
            if user becomes part of feature test/rollout
            If UserStorage is used, it will look into it for the
                variation and if found, no further processing is done

        Args:
            campaign_key (string): unique campaign test key
            user_id (string): ID assigned to a user

        Returns:
            Booleann: True if user becomes part of feature test/rollout,
            otherwise false in case user doesn't becomes part of it.
        """

        try:
            if not validate_util.is_valid_string(campaign_key) or not validate_util.is_valid_string(user_id):
                # log invalid params
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.IS_FEATURE_ENABLED_API_MISSING_PARAMS.format(
                        file=FILE
                    )
                )
                return False

            if not self.is_valid:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.IS_FEATURE_ENABLED_API_CONFIG_CORRUPTED.format(
                        file=FILE
                    )
                )
                return False

            # Get the campaign settings
            campaign = campaign_util.get_campaign(self.settings_file,
                                                  campaign_key)

            # Validate campaign
            if not campaign or campaign.get('status') != constants.STATUS_RUNNING:
                # log error
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(
                        file=FILE,
                        campaign_key=campaign_key,
                        api_name='is_feature_enabled'
                    )
                )
                return False

            # Validate campaign_type
            campaign_type = campaign.get('type')

            if campaign_type == constants.CAMPAIGN_TYPES.VISUAL_AB:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                        file=FILE,
                        api_name='is_feature_enabled',
                        user_id=user_id,
                        campaign_key=campaign_key,
                        campaign_type=campaign_type
                    )
                )
                return False

            # Get variation
            variation = self.variation_decider.get_variation(user_id,
                                                             campaign,
                                                             campaign_key
                                                             )

            # If no variation, did not become part of feature_test/rollout
            if not variation:
                return False

            # if campaign type is feature_test Send track call to server
            if campaign_type == constants.CAMPAIGN_TYPES.FEATURE_TEST:
                impression = impression_util.create_impression(self.settings_file,
                                                               campaign.get('id'),
                                                               variation.get('id'),
                                                               user_id)
                self.event_dispatcher.dispatch(impression)

            return True
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    api_name='is_feature_enabled',
                    exception=e
                )
            )

    def get_feature_variable_value(self, campaign_key, variable_key, user_id):
        """ Returns the feature variable corresponding to the variable_key
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
            campaign_key (string): unique campaign test key
            variable_key (string): variable key
            user_id (string): ID assigned to a user

        Returns:
            variable(bool, str, int, float)|None: If variation is assigned then
            variable corresponding to variation assigned else None
        """

        try:
            if not validate_util.is_valid_string(campaign_key) or \
                not validate_util.is_valid_string(variable_key) or \
                    not validate_util.is_valid_string(user_id):
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.GET_FEATURE_VARIABLE_MISSING_PARAMS.format(
                        file=FILE
                    )
                )
                return None

            if not self.is_valid:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.GET_FEATURE_VARIABLE_CONFIG_CORRUPTED.format(
                        file=FILE
                    )
                )
                return None

            # Get the campaign settings
            campaign = campaign_util.get_campaign(self.settings_file,
                                                  campaign_key)

            # Validate campaign
            if not campaign or campaign.get('status') != constants.STATUS_RUNNING:
                # log error
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.CAMPAIGN_NOT_RUNNING.format(
                        file=FILE,
                        campaign_key=campaign_key,
                        api_name='get_feature_variable_value'
                    )
                )
                return None

            campaign_type = campaign.get('type')

            if campaign_type == constants.CAMPAIGN_TYPES.VISUAL_AB:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.INVALID_API.format(
                        file=FILE,
                        api_name='get_feature_variable',
                        campaign_key=campaign_key,
                        campaign_type=campaign_type,
                        user_id=user_id
                    )
                )
                return None

            variation = self.variation_decider.get_variation(user_id,
                                                             campaign,
                                                             campaign_key
                                                             )

            # Check if variation has been assigned to user
            if not variation:
                return None

            # Variation recieved, find variable
            variable = None

            if campaign_type == constants.CAMPAIGN_TYPES.FEATURE_ROLLOUT:
                variables = campaign.get('variables')

            elif campaign_type == constants.CAMPAIGN_TYPES.FEATURE_TEST:
                if variation.get('isFeatureEnabled') is False:
                    self.logger.log(
                        LogLevelEnum.INFO,
                        LogMessageEnum.INFO_MESSAGES.FEATURE_NOT_ENABLED_FOR_USER.format(
                            file=FILE,
                            feature_key=campaign_key,
                            user_id=user_id
                        )
                    )
                    variation = campaign_util.get_control_variation(campaign)
                else:
                    self.logger.log(
                        LogLevelEnum.INFO,
                        LogMessageEnum.INFO_MESSAGES.FEATURE_ENABLED_FOR_USER.format(
                            file=FILE,
                            feature_key=campaign_key,
                            user_id=user_id
                        )
                    )
                variables = variation.get('variables')

            variable = campaign_util.get_variable(variables, variable_key)

            if not variable:
                # Log variable not found
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.VARIABLE_NOT_FOUND.format(
                        file=FILE,
                        variable_key=variable_key,
                        campaign_key=campaign_key,
                        campaign_type=campaign_type,
                        user_id=user_id
                    )
                )
                return None

            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.VARIABLE_FOUND.format(
                    file=FILE,
                    variable_key=variable_key,
                    variable_value=variable.get('value'),
                    campaign_key=campaign_key,
                    campaign_type=campaign_type,
                    user_id=user_id
                )
            )

            return feature_util.get_type_casted_feature_value(variable.get('value'),
                                                              variable.get('type'))

        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    api_name='get_feature_variable',
                    exception=e
                )
            )
