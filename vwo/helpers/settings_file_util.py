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

""" Module integrated in the vwo sdk for retrieving settings_file from the server
"""

from __future__ import print_function
import sys
import requests
from ..constants import constants
from ..helpers import generic_util, validate_util


def get(account_id, sdk_key, is_via_webhook=False):
    """ Get method to retrieve settings_file for customer from our server

    Args:
        account_id (string): Account ID of user
        sdk_key (string): Unique sdk key for user,
            can be retrieved from our webside
        is_via_webhook (bool): is triggered via webhook flag

    Returns:
        json_string|None: stringified json representing the settings_file,
            as received from the website,
            None if no settings_file is found or sdk_key is incorrect
    """

    is_valid_account_id = validate_util.is_valid_number(account_id) or validate_util.is_valid_string(account_id)

    if not is_valid_account_id or not validate_util.is_valid_string(sdk_key):
        print(("account_id and sdk_key are required", "for fetching account settings. Aborting!"), file=sys.stderr)
        return "{}"

    protocol = constants.HTTPS_PROTOCOL
    hostname = constants.ENDPOINTS.BASE_URL
    path = constants.ENDPOINTS.WEBHOOKS_ACCOUNT_SETTINGS if is_via_webhook else constants.ENDPOINTS.ACCOUNT_SETTINGS

    parameters = {
        "a": account_id,
        "i": sdk_key,
        "r": generic_util.get_random_number(),
        "platform": constants.PLATFORM,
        "api-version": constants.API_VERSION,
        "sdk": constants.SDK_NAME,
        "sdk-v": constants.SDK_VERSION,
    }
    server_url = protocol + hostname + path
    try:
        settings_file_response = requests.get(server_url, params=parameters)
        if settings_file_response.status_code != 200:
            print(
                "Request failed for fetching account settings. "
                "{via_webhook_message}"
                "Got Status Code: {status_code} "
                "and message: {settings_file_response}.".format(
                    via_webhook_message="[via Webhook] " if is_via_webhook else "",
                    status_code=settings_file_response.status_code,
                    settings_file_response=settings_file_response.text,
                ),
                file=sys.stderr,
            )
        settings_file = settings_file_response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching Settings File", e, file=sys.stderr)
        return "{}"
    return settings_file
