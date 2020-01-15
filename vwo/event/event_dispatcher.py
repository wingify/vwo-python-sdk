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

from ..http.connection import Connection
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger.logger_manager import VWOLogger

FILE = FileNameEnum.Event.EventDispatcher


class EventDispatcher(object):
    """ Class having request making/event dispatching capabilities to our servers"""

    def __init__(self, is_development_mode=False):
        """ Initialize the dispatcher with logger

        Args:
            is_development_mode: To specify whether the request
            to our server should be made or not.
        """
        self.logger = VWOLogger.getInstance()
        self.is_development_mode = is_development_mode
        self.connection = Connection()

    # The method dispatch has references from "Optimizely Python SDK, version 3.2.0",
    # Copyright 2016-2019, Optimizely, used under Apache 2.0 License.
    # Source - https://github.com/optimizely/python-sdk/blob/master/optimizely/event_dispatcher.py
    def dispatch(self, impression):
        """ Dispatch the event represented by the impression object.

        Args:
            event (dict): Object holding information about
            he request to be dispatched to the VWO backend.

        Returns:
            bool: True for success, false for failure
        """
        url = impression.pop('url')
        if self.is_development_mode:
            result = True
        else:
            resp = self.connection.get(url, params=impression)
            result = resp.get('status_code') == 200

        if result is True:
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.IMPRESSION_SUCCESS.format(
                    file=FILE,
                    end_point=url,
                )
            )
            return True
        else:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.IMPRESSION_FAILED.format(
                    file=FILE,
                    end_point=url,
                )
            )
            return False
