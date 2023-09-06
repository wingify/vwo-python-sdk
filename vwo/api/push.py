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

from ..helpers import custom_dimensions_util
from ..constants import constants
from ..constants.constants import API_METHODS
from ..helpers import validate_util, impression_util
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum

FILE = FileNameEnum.Api.Push


def _push(vwo_instance, tag_key="", tag_value="", user_id="", custom_dimension_map=None):
    """This API method: Makes a call to our server to store the tag_values

    1. Validates the arguments being passed
    2. Send a call to our server

    Args:
        tag_key (string): key name of the tag
          or
        custom_dimension_map (dict|None): Dict of tag keys vs values

        tag_value (string): value of the tag
        user_id (string): ID of the user for which value should be stored

    Returns:
        bool : True if call is made successfully, else False
    """

    vwo_instance.logger.set_api(API_METHODS.PUSH)

    if vwo_instance.is_opted_out:
        vwo_instance.logger.log(
            LogLevelEnum.INFO, LogMessageEnum.INFO_MESSAGES.API_NOT_ENABLED.format(file=FILE, api=API_METHODS.PUSH)
        )

        return False

    is_multiple_custom_dimension_used = False

    # Argument reshuffling
    if (
        tag_key
        and validate_util.is_valid_dict(tag_key)
        and validate_util.is_valid_string(tag_value)
        and not validate_util.is_valid_string(user_id)
    ):
        is_multiple_custom_dimension_used = True
        custom_dimension_map = tag_key
        user_id = tag_value

    if (
        (custom_dimension_map and not validate_util.is_valid_dict(custom_dimension_map))
        or (not custom_dimension_map and not validate_util.is_valid_string(tag_key))
        or (not custom_dimension_map and not validate_util.is_valid_string(tag_value))
        or not validate_util.is_valid_string(user_id)
    ):
        vwo_instance.logger.log(
            LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.PUSH_API_INVALID_PARAMS.format(file=FILE)
        )
        return False

    if not is_multiple_custom_dimension_used and len(tag_key) > constants.PUSH_API.TAG_KEY_LENGTH:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.TAG_KEY_LENGTH_EXCEEDED.format(file=FILE, user_id=user_id, tag_key=tag_key),
        )
        return False

    if not is_multiple_custom_dimension_used and len(tag_value) > constants.PUSH_API.TAG_VALUE_LENGTH:
        vwo_instance.logger.log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.TAG_VALUE_LENGTH_EXCEEDED.format(
                file=FILE, user_id=user_id, tag_value=tag_value
            ),
        )
        return False

    if not custom_dimension_map:
        custom_dimension_map = dict([(tag_key, tag_value)])

    if not vwo_instance.is_event_arch_enabled or vwo_instance.is_event_batching_enabled is True:

        for key, value in custom_dimension_map.items():
            impression = custom_dimensions_util.get_url_params(vwo_instance.settings_file, key, value, user_id)

            vwo_instance.event_dispatcher.dispatch(impression)

            vwo_instance.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.MAIN_KEYS_FOR_PUSH_API.format(
                    file=FILE,
                    u=impression.get("u"),
                    account_id=impression.get("account_id"),
                    tags=impression.get("tags"),
                ),
            )
    else:
        params = impression_util.get_events_params(
            vwo_instance.settings_file, constants.EVENTS.VWO_SYNC_VISITOR_PROP, user_agent=None, user_ip_address=None
        )
        impression = impression_util.create_push_events_impression(
            vwo_instance.settings_file, user_id, custom_dimension_map
        )
        vwo_instance.event_dispatcher.dispatch_events(params=params, impression=impression)

    return True
