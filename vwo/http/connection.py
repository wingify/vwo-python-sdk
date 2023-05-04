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

""" Module for making requests, uses requests internally """

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, Timeout, ConnectionError
from urllib3.util.retry import Retry

from ..logger import VWOLogger
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum

FILE = FileNameEnum.Http.Connection


class Connection:
    """Connection class to provide SDK with network connectivity interfaces"""

    def __init__(self):
        """Initializes connection class with requests session object"""
        self.logger = VWOLogger.getInstance()

        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            raise_on_status=False,
            connect=3,  # Retry on connection-related errors
            read=3,  # Retry on read-related errors
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, url, params=None):
        """Get method, it wraps upon requests' get method.
        Args:
            url (str): Unique resource locator
            params (dict): Parameters to be passed
        Returns:
            dict : Status code and Response text
        """
        try:
            resp = self.session.get(url, params=params)
            return {"status_code": resp.status_code, "text": resp.text}
        except Timeout as err:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CONNECTION_ERROR.format(file=FILE, reason="Timeout Exception", err=err),
            )

            return {"status_code": None, "text": ""}
        except ConnectionError as err:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CONNECTION_ERROR.format(
                    file=FILE, reason="Connection Error Exception", err=err
                ),
            )

            return {"status_code": None, "text": ""}
        except RequestException as err:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CONNECTION_ERROR.format(file=FILE, reason="Request Exception", err=err),
            )

            return {"status_code": None, "text": ""}
        except Exception as err:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CONNECTION_ERROR.format(file=FILE, reason="Exception", err=err),
            )

            return {"status_code": None, "text": ""}

    def post(self, url, params=None, data=None, headers=None):
        """Post method, it wraps upon requests' post method.
        Args:
            url (str): Unique resource locator
            params (dict): Parameters to be passed
            data (dict): Json data to be passed
            headers (dict): Headers for request
        Returns:
            dict : Status code and Response text
        """
        try:
            resp = self.session.post(url, params=params, json=data, headers=headers)
            return {"status_code": resp.status_code, "text": resp.text}
        except Timeout as err:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CONNECTION_ERROR.format(file=FILE, reason="Timeout", err=err),
            )

            return {"status_code": None, "text": ""}
        except ConnectionError as err:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CONNECTION_ERROR.format(file=FILE, reason="Connection Error", err=err),
            )

            return {"status_code": None, "text": ""}
        except RequestException as err:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CONNECTION_ERROR.format(file=FILE, reason="Request Exception", err=err),
            )

            return {"status_code": None, "text": ""}
        except Exception as err:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.CONNECTION_ERROR.format(file=FILE, reason="Exception", err=err),
            )

            return {"status_code": None, "text": ""}
