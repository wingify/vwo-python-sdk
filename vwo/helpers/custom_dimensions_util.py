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


from ..helpers import impression_util
from ..constants import constants
from ..logger import VWOLogger
from ..enums.log_level_enum import LogLevelEnum
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
import json

FILE = FileNameEnum.Helpers.CustomDimensionsUtil


def get_url_params(settings_file, tag_key, tag_value, user_id):
    """Creates a property object for custom dimension push api

    Args:
        settings_file (dict): settings_file consisting all the campaign related data
        tag_key (str): str value of length not greater than 255
        tag_value (str): str value of length not greater than 255
        user_id (str): unique user identifier for which custom dimensions should be stored

    Returns:
        dict : dict of all the required properties
    """
    url = constants.HTTPS_PROTOCOL + constants.ENDPOINTS.BASE_URL + constants.ENDPOINTS.PUSH
    tag = {"u": {tag_key: tag_value}}

    params = impression_util.get_common_properties(user_id, settings_file)
    params.update(url=url, tags=json.dumps(tag))

    VWOLogger.getInstance().log(
        LogLevelEnum.DEBUG,
        LogMessageEnum.DEBUG_MESSAGES.PARAMS_FOR_PUSH_CALL.format(
            file=FILE, properties=impression_util.get_stringified_log_impression(params)
        ),
    )
    return params
