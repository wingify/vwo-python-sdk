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

from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..enums.log_message_enum import LogMessageEnum
from ..helpers import validate_util
from ..services.usage_stats_manager import UsageStats
from ..vwo import VWO
from ..logger import VWOLogger

FILE = FileNameEnum.Api.Launch


def launch(settings_file, logger=None, user_storage=None, is_development_mode=False, **kwargs):
    """Launch api is the gateway to the SDK, it accepts all the launch parameters and
    initializes required services for the SDK, like logger, event_dispatcher, etc, and
    returns a VWO instance.

    Args:
        settings_file (json_string): stringified json representing the settings_file consisting all
            the campaign related data
        logger (object): an object capable of logging events happening inside the SDK
        user_storage (object): a storage service object capable of doing get and set on
        SDK provide data
        is_development_mode (bool): should the SDK be initialized in development mode,
        it toggles the event_dispatcher to off

    Keyword Args:
        log_level (vwo.LOG_LEVELS): a log_level with which SDK should be initialized.
        Default value is vwo.LOG_LEVELS.ERROR
        goal_type_to_track (vwo.GOAL_TYPES): which goal type to track when using track
        api. Default value is vwo.GOAL_TYPES.ALL
        batch_events (dict): settings for configuring and enabling event batching
        integrations (object): an integrations service instance for third party integrations


    Returns:
        VWO object: Successfully creates and returns a VWO object with passed params
        if all the params are valid else None
    """
    VWOLogger.clearExistingLoggerInstance()

    log_level = kwargs.get("log_level")
    goal_type_to_track = kwargs.get("goal_type_to_track")
    batch_event_settings = kwargs.get("batch_events")
    integrations = kwargs.get("integrations")

    invalid_log_level = False
    if log_level and not validate_util.is_valid_log_level(log_level):
        log_level = None
        invalid_log_level = True

    invalid_logger = False
    if logger and not validate_util.is_valid_service(logger, "logger"):
        logger = None
        invalid_logger = True
    module_logger = VWOLogger.getInstance(log_level=log_level, logger=logger)

    if (
        invalid_log_level
        or invalid_logger
        or (user_storage and not validate_util.is_valid_service(user_storage, "user_storage"))
        or not validate_util.is_valid_settings_file(settings_file)
        or (is_development_mode and type(is_development_mode) is not bool)
        or (goal_type_to_track and not validate_util.is_valid_goal_type(goal_type_to_track))
        or (
            batch_event_settings
            and not validate_util.is_valid_batch_event_settings(val=batch_event_settings, file=FILE)
        )
        or (integrations and not validate_util.is_valid_service(integrations, "integrations"))
    ):
        module_logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.LAUNCH_API_INVALID_PARAMS.format(file=FILE))
        return None
    else:
        module_logger.log(LogLevelEnum.DEBUG, LogMessageEnum.DEBUG_MESSAGES.VALID_CONFIGURATION.format(file=FILE))
        if not is_development_mode:
            UsageStats.collect_usage_stats(
                batch_event_settings=batch_event_settings,
                integrations=integrations,
                storage_service=user_storage,
                logger=logger,
                log_level=log_level,
                goal_type_to_track=goal_type_to_track,
            )
        return VWO(
            settings_file, user_storage, is_development_mode, goal_type_to_track, batch_event_settings, integrations
        )
