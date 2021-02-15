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

import json
from ..helpers.settings_file_util import get as get_settings_file
from ..helpers import validate_util
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..helpers import campaign_util
from ..logger import VWOLogger

FILE = FileNameEnum.Services.SettingsFileManager


class SettingsFileManager(object):
    """ VWO settings_file manager """

    def __init__(self, settings_file):
        """ Init method to load and set vwo object with settings_file data.

        Args:
            settings_file (json_string): stringified json representing the vwo settings_file.
        """
        self.logger = VWOLogger.getInstance()
        self.update_settings_file(settings_file)

    # PUBLIC METHODS
    def process_settings_file(self):
        """ Processes the settings_file, assigns variation allocation range """

        settings_file = self.settings_file
        for campaign in settings_file.get("campaigns"):
            campaign_util.set_variation_allocation(campaign)
        self.logger.log(LogLevelEnum.DEBUG, LogMessageEnum.DEBUG_MESSAGES.SETTINGS_FILE_PROCESSED.format(file=FILE))

    def get_settings_file(self):
        """ Retrieves settings file """

        return self.settings_file

    def get_settings_file_string(self):
        """ Retrieves stringified json representing the settings_file """

        return self.settings_file_string

    def get_and_update_settings_file(self, account_id, sdk_key, is_via_webhook):
        """ 
        Fetch latest settings_file and update so that vwo_instance could use the latest settings

        Args:
            account_id (string): Account ID of user
            sdk_key (string): Unique sdk key for user,
                can be retrieved from our webside
            is_via_webhook (bool): is triggered via webhook flag:

        Returns:
            bool: True if settings_file is updated else False
        """
        
        latest_settings_file = get_settings_file(account_id, sdk_key, is_via_webhook)

        if not validate_util.is_valid_settings_file(latest_settings_file):
            self.logger.log(
                LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.INVALID_SETTINGS_FILE.format(file=FILE, account_id=account_id),
            )
            return False

        if latest_settings_file == self.settings_file_string:
            self.logger.log(
                LogLevelEnum.INFO, LogMessageEnum.INFO_MESSAGES.SETTINGS_FILE_NOT_UPDATED.format(file=FILE),
            )
            return False

        self.update_settings_file(latest_settings_file)
        return True

    def update_settings_file(self, settings_file):
        """ Update the settings_file on the instance so that latest settings could be used 
        from next hit onwards
        
        Args:
            settings_file (json_string): stringified json representing the settings_file, 
                as received from the website
        """
        self.settings_file_string = settings_file
        self.settings_file = json.loads(settings_file)
        self.process_settings_file()
