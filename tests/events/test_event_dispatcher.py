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

import mock
import unittest
import time

from vwo.event import event_dispatcher
from ..data.constants import TEST_ACCOUNT_ID
from vwo.constants import constants
from vwo.services.url_manager import url_manager


def flush_callback(err, events):
    pass


test_properties = {
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

test_events_track_impression_properties = {
    "d": {
        "msgId": "09CD6107E42B51F9BFC3DD97EA900990-1565949670",
        "visId": "09CD6107E42B51F9BFC3DD97EA900990",
        "sessionId": 1633330743,
        "event": {
            "props": {
                "$visitor": {"props": {"vwo_fs_environment": "testenvkey123456789472c212c972e"}},
                "sdkName": constants.SDK_NAME,
                "sdkVersion": constants.SDK_VERSION,
                "variation": 2,
                "isFirst": 1,
            },
            "name": constants.EVENTS.VWO_VARIATION_SHOWN,
            "time": 1565949670344,
        },
        "visitor": {"props": {"vwo_fs_environment": "testenvkey123456789472c212c972e"}},
    }
}

test_events__track_query_params_properties = {
    "en": constants.EVENTS.VWO_VARIATION_SHOWN,
    "a": TEST_ACCOUNT_ID,
    "env": "testenvkey123456789472c212c972e",
    "eTime": 1565949670344,
    "random": 0.7382938446947298,
    "ig": 1,
    "ss": 1,
    "ll": 1,
    "_l": 1,
    "id": 10,
}

test_event_batching_settings = {"events_per_request": 5, "request_time_interval": 1, "flush_callback": flush_callback}


class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.dispatcher = event_dispatcher.EventDispatcher()
        self.async_dispatcher = event_dispatcher.EventDispatcher(
            batch_event_settings=test_event_batching_settings, sdk_key="sample_key"
        )

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

    def test_dispatch_sends_events_impression(self):
        url = constants.HTTPS_PROTOCOL + url_manager.get_base_url() + constants.ENDPOINTS.EVENTS
        with mock.patch(
            "vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}
        ) as mock_connection_get:
            result = self.dispatcher.dispatch_events(
                params=test_events__track_query_params_properties, impression=test_events_track_impression_properties
            )
            self.assertIs(result, True)
        mock_connection_get.assert_called_once_with(
            url,
            params=test_events__track_query_params_properties,
            data=test_events_track_impression_properties,
            headers={"User-Agent": constants.SDK_NAME},
        )

    def test_dispatch_events_returns_error_status_code(self):
        with mock.patch("vwo.http.connection.Connection.post", return_value={"status_code": 503}):
            result = self.dispatcher.dispatch_events(
                params=test_events__track_query_params_properties, impression=test_events_track_impression_properties
            )
            self.assertIs(result, False)

    def test_event_batching_dispatch_sends_event(self):
        with mock.patch("vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}):
            self.assertIs(len(self.async_dispatcher.queue), 0)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 1)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 2)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 3)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 4)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 0)

    def test_event_batching_dispatch_sends_diff_events(self):
        with mock.patch("vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}):
            track_goal_event = test_properties.copy()
            track_goal_event["url"] = "https://dev.visualwebsiteoptimizer.com/server-side/track-goal"
            track_goal_event["r"] = "abcd"

            push_event = test_properties.copy()
            push_event["url"] = "https://dev.visualwebsiteoptimizer.com/server-side/push"

            self.async_dispatcher.dispatch(test_properties.copy())
            self.async_dispatcher.dispatch(test_properties.copy())
            self.async_dispatcher.dispatch(test_properties.copy())
            self.async_dispatcher.dispatch(track_goal_event)
            self.async_dispatcher.dispatch(push_event)
            self.assertIs(len(self.async_dispatcher.queue), 0)

    def test_event_batching_dispatch_sends_event_413_repsonse(self):
        with mock.patch("vwo.http.connection.Connection.post", return_value={"status_code": 413, "text": ""}):
            self.assertIs(len(self.async_dispatcher.queue), 0)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 1)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 2)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 3)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 4)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 0)

    def test_event_batching_dispatch_sends_event_500_repsonse(self):
        with mock.patch("vwo.http.connection.Connection.post", return_value={"status_code": 500, "text": ""}):
            self.assertIs(len(self.async_dispatcher.queue), 0)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 1)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 2)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 3)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 4)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 0)

    def test_event_batching_dispatch_sends_event_with_timer(self):
        with mock.patch("vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}):
            self.assertIs(len(self.async_dispatcher.queue), 0)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 1)
            self.async_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.async_dispatcher.queue), 2)
            time.sleep(1.1)
            self.assertIs(len(self.async_dispatcher.queue), 0)

    def test_event_batching_with_error(self):
        with mock.patch("vwo.event.event_dispatcher.EventDispatcher.async_dispatch", return_value=False):
            self.async_dispatcher.dispatch(test_properties.copy())

    def test_event_batching_with_error_2(self):
        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.update_queue_metadata", side_effect=Exception("Test")
        ):
            self.async_dispatcher.dispatch(test_properties.copy())
