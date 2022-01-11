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

from ..constants.constants import API_METHODS
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..enums.log_message_enum import LogMessageEnum

FILE = FileNameEnum.Api.FlushEvents


def _flush_events(vwo_instance, mode):
    """ This API method: Flushes the queue and syncs the events to VWO
        servers.

    Args:
        mode(string): In sync mode, function makes a synchronous call before exiting
            In async mode, function spawns a thread to sync to VWO and exits
    """
    if vwo_instance.is_opted_out:
        vwo_instance.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.API_NOT_ENABLED.format(file=FILE, api=API_METHODS.FLUSH_EVENTS),
        )

        return False

    if vwo_instance.is_event_batching_enabled:
        vwo_instance.logger.set_api(API_METHODS.FLUSH_EVENTS)
        vwo_instance.event_dispatcher.flush_queue(manual=True, mode=mode)

        return True
