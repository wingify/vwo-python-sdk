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

from ..enums.log_message_enum import LogMessageEnum
from ..enums.log_level_enum import LogLevelEnum
from ..enums.file_name_enum import FileNameEnum
from ..logger import VWOLogger


FILE = FileNameEnum.Services.HooksManager

class HooksManager(object):
  """
  Hooks Manager is responsible for triggering callbacks useful to the end-user
  based on certain lifecycle events. Possible use with integrations when the user 
  intends to send an event when a visitor is part of the experiment.
  """

  def __init__(self, intgerations):
    """
    Initializes HooksManager with an integrations service instance.

    Args:
      integrations (dict): an integrations service instance for third party integrations
    """
    self.logger = VWOLogger.getInstance()
    self.integrations = intgerations
  
  def execute(self, properties):
    """
    Executes the callback

    Args:
      properties (dict): data to be send as a parameter in callback
    """

    if self.integrations.callback is not None and callable(self.integrations.callback):
      try:
        self.integrations.callback(properties)
      except Exception as e:
        self.logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.INTEGRATIONS_SERVICE_CALLBACK_EXECUTION_ERROR.format(file=FILE, error_message=e))
    else:
        self.logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.INTEGRATIONS_SERVICE_CALLBACK_INVALID.format(file=FILE))

