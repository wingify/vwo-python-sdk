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

from __future__ import print_function
import unittest
import json
import random
import mock

import vwo
from vwo.constants import constants
from ..data.settings_files import SETTINGS_FILES
from ..data.constants import TEST_ACCOUNT_ID
from ..config.config import TEST_LOG_LEVEL


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

test_event_batching_settings = {"events_per_request": 5, "request_time_interval": 1, "flush_callback": flush_callback}


class FlushTest(unittest.TestCase):
    def set_up(self, config_variant="AB_T_50_W_50_50", event_batching_settings=None):
        self.user_id = str(random.random())
        self.settings_file = json.dumps(SETTINGS_FILES.get(config_variant))
        self.vwo = vwo.launch(
            self.settings_file,
            is_development_mode=False,
            log_level=TEST_LOG_LEVEL,
            batch_events=event_batching_settings,
        )

    def test_flush_sync(self):
        self.set_up(event_batching_settings=test_event_batching_settings)
        with mock.patch(
            "vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}
        ) as mock_connection_post:
            self.assertIs(len(self.vwo.event_dispatcher.queue), 0)
            self.vwo.event_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.vwo.event_dispatcher.queue), 1)
            self.vwo.event_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.vwo.event_dispatcher.queue), 2)
            self.vwo.flush_events(mode="sync")
            self.assertIs(len(self.vwo.event_dispatcher.queue), 0)
        mock_connection_post.assert_called_once()

    def test_flush_async(self):
        self.set_up(event_batching_settings=test_event_batching_settings)
        with mock.patch("vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}):
            self.assertIs(len(self.vwo.event_dispatcher.queue), 0)
            self.vwo.event_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.vwo.event_dispatcher.queue), 1)
            self.vwo.event_dispatcher.dispatch(test_properties.copy())
            self.assertIs(len(self.vwo.event_dispatcher.queue), 2)
            self.vwo.flush_events(mode="async")
            self.assertIs(len(self.vwo.event_dispatcher.queue), 0)

    def test_flush_with_no_events(self):
        self.set_up(event_batching_settings=test_event_batching_settings)
        with mock.patch("vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}):
            self.vwo.flush_events(mode="sync")

    def test_flush_queue_without_enabling_event_batching(self):
        self.set_up()
        with mock.patch("vwo.http.connection.Connection.post", return_value={"status_code": 200, "text": ""}):
            self.vwo.flush_events(mode="sync")

    def test_event_batching_with_error(self):
        self.set_up(event_batching_settings=test_event_batching_settings)
        with mock.patch("vwo.http.connection.Connection.post", side_effect=Exception("Test")):
            self.vwo.event_dispatcher.dispatch(test_properties.copy())
            self.vwo.flush_events(mode="sync")
