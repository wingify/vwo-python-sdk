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

import json
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..helpers import campaign_util
from ..logger.logger_manager import VWOLogger

FILE = FileNameEnum.Services.SettingsFileManager


class SettingsFileManager(object):
    """ VWO settings_file manager """

    def __init__(self, settings_file):
        """ Init method to load and set vwo object with settings_file data.

        Args:
            settings_file (dict): Dict object
                representing the vwo settings_file.
        """
        self.settings_file = json.loads(settings_file)
        self.logger = VWOLogger.getInstance()

    # PUBLIC METHODS

    def process_settings_file(self):
        """ Processes the settings_file, assigns variation allocation range """

        settings_file = self.settings_file
        for campaign in settings_file.get('campaigns'):
            campaign_util.set_variation_allocation(campaign)
        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.SETTINGS_FILE_PROCESSED.format(
                file=FILE
            )
        )

    def get_settings_file(self):
        """ Retrieves settings file """

        return self.settings_file
