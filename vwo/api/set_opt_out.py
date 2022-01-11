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

from ..constants.constants import API_METHODS
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum

FILE = FileNameEnum.Api.SET_OPT_OUT


def _set_opt_out(vwo_instance):
    """
    Calling this API will opt out VWO from tracking
    Any further API call will simply return until SDK is reinitialized

    Returns:
        bool : True if opted out from VWO Tracking
    """

    vwo_instance.logger.set_api(API_METHODS.SET_OPT_OUT)

    vwo_instance.logger.log(LogLevelEnum.INFO, LogMessageEnum.INFO_MESSAGES.OPT_OUT_API_CALLED.format(file=FILE))

    vwo_instance.is_opted_out = True
    vwo_instance.settings_file = None

    if vwo_instance.is_event_batching_enabled:
        vwo_instance.event_dispatcher.flush_queue(manual=True, mode="sync")

    vwo_instance.event_dispatcher = None
    vwo_instance.variation_decider = None
    vwo_instance.config = None

    return True
