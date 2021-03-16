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

from . import api
from .core.variation_decider import VariationDecider
from .enums.file_name_enum import FileNameEnum
from .enums.log_level_enum import LogLevelEnum
from .enums.log_message_enum import LogMessageEnum
from .event.event_dispatcher import EventDispatcher
from .helpers.generic_util import safe_method
from .logger import VWOLogger
from .services.settings_file_manager import SettingsFileManager
from .constants.constants import GOAL_TYPES


FILE = FileNameEnum.Vwo.VWO
logger = VWOLogger.getInstance()


class VWO(object):
    """ Core class of the SDK, consisting all the APIs featured in VWO Full Stack Server Side Testing """

    def __init__(
        self, settings_file, user_storage, is_development_mode, goal_type_to_track, should_track_returning_user, batch_event_settings, integrations
    ):
        """ __init__ method to initialize the VWO object, all the argument types should be pre-checked.
        Else object initialization fails.

        Args:
            settings_file (json_string): stringified json representing the settings_file consisting all
                the campaign related data
            user_storage (object): a storage service object capable of doing get and set on
            SDK provide data
            is_development_mode (bool): should the SDK be initialized in development mode,
            it toggles the event_dispatcher to off
            goal_type_to_track (vwo.GOAL_TYPES): which goal type to track when using track
            api. Default value is vwo.GOAL_TYPES.ALL
            should_track_returning_user (bool): should returning user be tracked again.
            Default value is False
            batch_events_settings (dict): settings for configuring and enabling event batching
            integrations (dict): an integrations service instance for third party integrations
        """
        self.logger = VWOLogger.getInstance()
        self.config = SettingsFileManager(settings_file)
        self.settings_file = self.config.get_settings_file()
        self.variation_decider = VariationDecider(user_storage, account_id=self.settings_file.get("accountId"), integrations=integrations)
        if is_development_mode:
            self.logger.log(LogLevelEnum.DEBUG, LogMessageEnum.DEBUG_MESSAGES.SET_DEVELOPMENT_MODE.format(file=FILE))
        self.event_dispatcher = EventDispatcher(is_development_mode=is_development_mode or False, batch_event_settings=batch_event_settings, sdk_key=self.settings_file.get("sdkKey"))
        self.goal_type_to_track = goal_type_to_track or GOAL_TYPES.ALL
        self.should_track_returning_user = should_track_returning_user or False
        self.logger.log(LogLevelEnum.DEBUG, LogMessageEnum.DEBUG_MESSAGES.SDK_INITIALIZED.format(file=FILE))

    # PUBLIC METHODS
    activate = safe_method(api._activate, None, FILE)
    get_variation_name = safe_method(api._get_variation_name, None, FILE)
    track = safe_method(api._track, False, FILE)
    is_feature_enabled = safe_method(api._is_feature_enabled, False, FILE)
    get_feature_variable_value = safe_method(api._get_feature_variable_value, None, FILE)
    push = safe_method(api._push, False, FILE)
    flush_events = safe_method(api._flush_events, False, FILE)
    get_and_update_settings_file = safe_method(api._get_and_update_settings_file, None, FILE)
