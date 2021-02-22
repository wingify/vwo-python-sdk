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

""" Module for making requests, uses requests internally """

import requests


class Connection:
    """ Connection class to provide SDK with network connectivity interfaces """

    def __init__(self):
        """ Initializes connection class with requests session object"""
        self.session = requests.Session()

    def get(self, url, params=None):
        """ Get method, it wraps upon requests' get method.
        Args:
            url (str): Unique resource locator
            params (dict): Parameters to be passed
        Returns:
            dict : Status code and Response text
        """
        try:
            resp = self.session.get(url, params=params)
            return {"status_code": resp.status_code, "text": resp.text}
        except Exception:
            return {"status_code": None, "text": ""}

    def post(self, url, params=None, data=None, headers=None):
        """ Post method, it wraps upon requests' post method.
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
        except Exception:
            return {"status_code": None, "text": ""}
