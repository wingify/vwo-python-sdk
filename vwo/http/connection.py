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

""" Module for making requests, uses requests internally """

import requests


class Connection:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url, params=None):
        try:
            resp = self.session.get(url, params=params)
            return {
                'status_code': resp.status_code,
                'text': resp.text
            }
        except Exception:
            return {
                'status_code': None,
                'text': ''
            }

    def post(self, url, params=None, data=None):
        try:
            resp = self.session.post(url, params=params, json=data)
            return {
                'status_code': resp.status_code,
                'text': resp.text
            }
        except Exception:
            return {
                'status_code': None,
                'text': ''
            }
