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
import time

from vwo.event import event_dispatcher
from ..data.constants import TEST_ACCOUNT_ID, TEST_USER_ID
from vwo.constants import constants

test_properties = {
    "uId": TEST_USER_ID,
    "combination": 1,
    "url": "https://dev.visualwebsiteoptimizer.com/server-side/track-user",
    "ed": '{"p": "%s"}' % constants.PLATFORM,
    "random": 0.7382938446947298,
    "ap": constants.PLATFORM,
    "u": "09CD6107E42B51F9BFC3DD97EA900990",
    "experiment_id": 229,
    "sId": 1565949670,
    "sdk-v": constants.SDK_VERSION,
    "sdk": constants.SDK_NAME,
    "account_id": TEST_ACCOUNT_ID,
}

test_event_batching_settings = {
    'events_per_request': 5,
    'request_time_interval': 1
}


class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.dispatcher = event_dispatcher.EventDispatcher()
        self.async_dispatcher = event_dispatcher.EventDispatcher(batch_event_settings=test_event_batching_settings, sdk_key="sample_key")

    def test_dispatch_sends_event(self):
        properties = test_properties.copy()
        properties_for_check = properties.copy()
        with mock.patch(
            "vwo.http.connection.Connection.get", return_value={"status_code": 200, "text": ""}
        ) as mock_connection_get:
            result = self.dispatcher.dispatch(properties)
            self.assertIs(result, True)
        url = properties_for_check.pop("url")
        mock_connection_get.assert_called_once_with(url, params=properties)

    def test_dispatch_returns_error_status_code(self):
        properties = test_properties.copy()
        with mock.patch("vwo.http.connection.Connection.get", return_value={"status_code": 503}):
            result = self.dispatcher.dispatch(properties)
            self.assertIs(result, False)

    def test_event_batching_dispatch_sends_event(self):
        with mock.patch(
            "vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}
        ) as mock_connection_post:
            self.assertIs(len(self.async_dispatcher.queue), 0)
            result = self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 1)
            result = self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 2)
            result = self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 3)
            result = self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 4)
            result = self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 0)
        mock_connection_post.assert_called_once()

    def test_event_batching_dispatch_sends_event_with_timer(self):
        with mock.patch(
            "vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}
        ) as mock_connection_post:
            self.assertIs(len(self.async_dispatcher.queue), 0)
            result = self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 1)
            result = self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 2)
            time.sleep(1.1)
            self.assertIs(len(self.async_dispatcher.queue), 0)
        mock_connection_post.assert_called_once()
