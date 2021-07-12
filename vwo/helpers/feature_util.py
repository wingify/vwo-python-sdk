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

""" Utility for managing feature related functionalities """

import json

from ..constants import constants
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger import VWOLogger

FILE = FileNameEnum.Helpers.FeatureUtil


def get_type_casted_feature_value(value, variable_type):
    """Returns type casted value to given value type if possbile.

    Args:
        value (int|float|str|bool): Value to type cast
        variable_type (type): Type to which value needs to be casted
    Returns:
        type_casted_value|None : Type casted value if value can be
        typecasted else None
    """

    # Check if type(value) is already equal to required variable_type
    if type(value) == constants.PY_VARIABLE_TYPES.get(variable_type):
        return value
    try:
        if variable_type == constants.VARIABLE_TYPES.STRING:
            return str(value)
        elif variable_type == constants.VARIABLE_TYPES.INTEGER:
            return int(value)
        elif variable_type == constants.VARIABLE_TYPES.DOUBLE:
            return float(value)
        elif variable_type == constants.VARIABLE_TYPES.JSON:
            return json.loads(value)
        else:
            # required type is boolean, simply raise exception
            # as it doesn't belong to bool type
            raise Exception
    except Exception:
        VWOLogger.getInstance().log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.UNABLE_TO_TYPE_CAST.format(
                file=FILE, value=value, variable_type=variable_type, of_type=type(value)
            ),
        )
        return None
