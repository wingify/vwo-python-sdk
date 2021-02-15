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
from ..constants.constants import API_METHODS

FILE = FileNameEnum.Api.GetAndUpdateSettingsFile


def _get_and_update_settings_file(vwo_instance, account_id, sdk_key, is_via_webhook=False):
    """ This API method: Makes a call to our server and fetch the latest settings_file
    and update the vwo_instance

    Args:
        account_id (string): Account ID of user
        sdk_key (string): Unique sdk key for user,
            can be retrieved from our webside
        is_via_webhook (bool): is triggered via webhook flag
    
    Returns:
        (json_string): stringified json representing the settings_file,
            as received from the website
    """
    vwo_instance.logger.set_api(API_METHODS.GET_AND_UPDATE_SETTINGS_FILE)

    is_settings_file_updated = vwo_instance.config.get_and_update_settings_file(account_id, sdk_key, is_via_webhook)

    if is_settings_file_updated:
        vwo_instance.settings_file = vwo_instance.config.get_settings_file()
        vwo_instance.logger.log(
            LogLevelEnum.INFO, LogMessageEnum.INFO_MESSAGES.SETTINGS_FILE_UPDATED.format(file=FILE),
        )
    
    return vwo_instance.config.get_settings_file_string()