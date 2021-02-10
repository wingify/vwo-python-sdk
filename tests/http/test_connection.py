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

import mock
import unittest
from vwo.http import connection


class Response:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


class ConnectionTest(unittest.TestCase):
    def setUp(self):
        self.connection = connection.Connection()

    def test_connection_get_with_exception(self):
        with mock.patch("requests.Session.get", side_effect=Exception("REQUEST FAILED")):
            result = self.connection.get("https://vwo.com/")
            self.assertDictEqual(result, {"status_code": None, "text": ""})

    def test_connection_get(self):
        resp = Response(200, "success")
        return_value = {"status_code": 200, "text": "success"}
        with mock.patch("requests.Session.get", return_value=resp):
            result = self.connection.get("https://vwo.com/")
            self.assertDictEqual(result, return_value)

    def test_connection_post_with_exception(self):
        with mock.patch("requests.Session.post", side_effect=Exception("REQUEST FAILED")):
            result = self.connection.post("https://vwo.com/")
            self.assertDictEqual(result, {"status_code": None, "text": ""})

    def test_connection_post(self):
        resp = Response(200, "success")
        return_value = {"status_code": 200, "text": "success"}
        with mock.patch("requests.Session.post", return_value=resp):
            result = self.connection.post("https://vwo.com/")
            self.assertDictEqual(result, return_value)
