""" Module integrated in the vwo sdk for retrieving settings_file from the server
"""

from __future__ import print_function
import sys
import requests
from ..constants import constants
from ..helpers import function_util, validate_util


def get(account_id, sdk_key):
    """ Get method to retrieve settings_file for customer from dacdn server

    Args:
        account_id (string): Acount ID of user
        sdk_key (string): Unique sdk key for user,
            can be retrieved from our webside

    Returns:
        json_string|None: Json representation of settings_file,
            as recieved from the website,
            None if no settings_file is found or sdk_key is incorrect
    """

    is_valid_sdk_key = validate_util.is_valid_number(account_id) or \
        validate_util.is_valid_string(account_id)

    if not is_valid_sdk_key or \
       not validate_util.is_valid_string(sdk_key):
        print(('account_id and sdk_key are required',
               'for fetching account settings. Aborting!'
               ), file=sys.stderr)
        return '{}'

    protocol = 'https'
    hostname = constants.ENDPOINTS.BASE_URL
    path = constants.ENDPOINTS.ACCOUNT_SETTINGS

    parameters = {
        'a': account_id,
        'i': sdk_key,
        'r': function_util.get_random_number(),
        'platform': 'server',
        'api-version': 2
    }
    dacdn_url = protocol + '://' + hostname + path
    try:
        settings_file_response = requests.get(
            dacdn_url,
            params=parameters
        )
        if settings_file_response.status_code != 200:
            print('Request failed for fetching account settings. '
                  'Got Status Code: {status_code} '
                  'and message: {settings_file_response}.'.
                  format(status_code=settings_file_response.status_code,
                         settings_file_response=settings_file_response.text
                         ),
                  file=sys.stderr
                  )
        settings_file = settings_file_response.text
    except requests.exceptions.RequestException as e:
        print('Error fetching Settings File', e, file=sys.stderr)
        return '{}'
    return settings_file
