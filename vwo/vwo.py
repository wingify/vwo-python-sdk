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

from . import api
from .core.variation_decider import VariationDecider
from .enums.file_name_enum import FileNameEnum
from .enums.log_level_enum import LogLevelEnum
from .enums.log_message_enum import LogMessageEnum
from .event.event_dispatcher import EventDispatcher
from .helpers import validate_util
from .logger.logger_manager import VWOLogger, configure_logger
from .services import singleton
from .services.settings_file_manager import SettingsFileManager

FILE = FileNameEnum.Vwo.VWO


class VWO(object):
    """ The VWO class which exposes all the SDK APIs for full stack
    server side optimization. """

    # The method __init__ has references from "Optimizely Python SDK, version 3.2.0",
    # Copyright 2016-2019, Optimizely, used under Apache 2.0 License.
    # Source - https://github.com/optimizely/python-sdk/blob/master/optimizely/optimizely.py
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
        # Remove all instances of Singleton logger
        singleton.forgetAllSingletons()

        # Retrieve log_level from kwargs
        if not logger:
            log_level = kwargs.get('log_level')
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
        self.variation_decider = VariationDecider(user_storage)

        # Assign event dispatcher
        if is_development_mode:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.SET_DEVELOPMENT_MODE.format(
                    file=FILE
                )
            )
        self.event_dispatcher = EventDispatcher(is_development_mode)

        # Log successfully initialized SDK
        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.SDK_INITIALIZED.format(
                file=FILE
            )
        )

    # PUBLIC METHODS

    def activate(self, campaign_key, user_id, **kwargs):
        try:
            return api._activate(self, campaign_key, user_id, kwargs=kwargs)
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    exception=e
                )
            )
            return None

    def get_variation_name(self, campaign_key, user_id, **kwargs):
        try:
            return api._get_variation_name(self, campaign_key, user_id, kwargs=kwargs)
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    exception=e
                )
            )
            return None

    def track(self, campaign_key, user_id, goal_identifier, **kwargs):
        try:
            return api._track(self, campaign_key, user_id, goal_identifier, kwargs=kwargs)
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    exception=e
                )
            )
            return False

    def is_feature_enabled(self, campaign_key, user_id, **kwargs):
        try:
            return api._is_feature_enabled(self, campaign_key, user_id, kwargs=kwargs)
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    exception=e
                )
            )
            return False

    def get_feature_variable_value(self, campaign_key, variable_key, user_id, **kwargs):
        try:
            return api._get_feature_variable_value(self, campaign_key, variable_key, user_id, kwargs=kwargs)
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    exception=e
                )
            )
            return None

    def push(self, tag_key, tag_value, user_id):
        try:
            return api._push(self, tag_key, tag_value, user_id)
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.API_NOT_WORKING.format(
                    file=FILE,
                    exception=e
                )
            )
            return False
