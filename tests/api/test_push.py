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
from ..data.settings_files import SETTINGS_FILES

from ..config.config import TEST_LOG_LEVEL


class PushTest(unittest.TestCase):
    def set_up(self, config_variant="AB_T_50_W_50_50"):
        self.user_id = str(random.random())
        self.settings_file = json.dumps(SETTINGS_FILES.get(config_variant))

        self.vwo = vwo.launch(self.settings_file, is_development_mode=True, log_level=TEST_LOG_LEVEL)
        self.campaign_key = config_variant
        try:
            self.goal_identifier = SETTINGS_FILES[config_variant]["campaigns"][0]["goals"][0]["identifier"]
        except Exception:
            pass

    def test_push_raises_exception(self):
        with mock.patch("vwo.helpers.validate_util.is_valid_string", side_effect=Exception("Test")):
            self.set_up()
            self.assertIs(False, self.vwo.push("SOME_CAMPAIGN", "VARIABLE_KEY", "USER_ID"))

    def test_push_true(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("DUMMY_SETTINGS_FILE")), log_level=TEST_LOG_LEVEL, is_development_mode=True
        )
        self.assertIs(True, vwo_instance.push("browser", "chrome", "12345"))

    def test_push_int_value_false(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("DUMMY_SETTINGS_FILE")), log_level=TEST_LOG_LEVEL, is_development_mode=True
        )
        self.assertIs(False, vwo_instance.push("browser", 1, "12345"))

    def test_push_with_invalid_custom_dimension_map(self):
        self.set_up("DUMMY_SETTINGS_FILE")

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            self.vwo.event_dispatcher.dispatch_events = mock.MagicMock()
            result = self.vwo.push(custom_dimension_map={}, user_id="12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 0)
            self.assertFalse(result)

            self.vwo.push(custom_dimension_map=[1, 2], user_id="12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 0)
            self.assertFalse(result)

            self.vwo.push(custom_dimension_map="invalid_custom_dimension_map", user_id="12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 0)
            self.assertFalse(result)
            self.vwo.push(custom_dimension_map=9999999, user_id="12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 0)
            self.assertFalse(result)

            mock_event_dispatcher_dispatch.reset_mock()
            self.vwo.event_dispatcher.dispatch_events.assert_not_called()

    def test_push_with_custom_dimension_map_without_event_arch_and_event_batching(self):
        self.set_up("DUMMY_SETTINGS_FILE")

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            self.vwo.event_dispatcher.dispatch_events = mock.MagicMock()
            self.vwo.push(custom_dimension_map={"tag_key_1": "tag_value_1"}, user_id="12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)
            self.vwo.push(
                custom_dimension_map={
                    "tag_key_1": "tag_value_1",
                    "tag_key_2": "tag_value_2",
                    "tag_key_3": "tag_value_3",
                },
                user_id="12345",
            )
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 4)
            mock_event_dispatcher_dispatch.reset_mock()
            self.vwo.event_dispatcher.dispatch_events.assert_not_called()

    def test_push_with_custom_dimension_map_and_event_arch_and_without_event_batching(self):
        self.set_up("DUMMY_SETTINGS_FILE")

        event_arch_settings_file = SETTINGS_FILES.get("DUMMY_SETTINGS_FILE").copy()
        event_arch_settings_file["isEventArchEnabled"] = True
        self.vwo = vwo.launch(json.dumps(event_arch_settings_file), is_development_mode=True, log_level=TEST_LOG_LEVEL)

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch_events", return_value=None
        ) as mock_event_dispatcher_dispatch_events:
            self.vwo.event_dispatcher.dispatch = mock.MagicMock()
            self.vwo.push(custom_dimension_map={"tag_key_1": "tag_value_1"}, user_id="12345")
            self.assertIs(mock_event_dispatcher_dispatch_events.call_count, 1)
            self.vwo.push(
                custom_dimension_map={
                    "tag_key_1": "tag_value_1",
                    "tag_key_2": "tag_value_2",
                    "tag_key_3": "tag_value_3",
                },
                user_id="12345",
            )
            self.assertIs(mock_event_dispatcher_dispatch_events.call_count, 2)
            mock_event_dispatcher_dispatch_events.reset_mock()
            self.vwo.event_dispatcher.dispatch.assert_not_called()

    def test_push_with_custom_dimension_map_positional_params(self):
        self.set_up("DUMMY_SETTINGS_FILE")

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            self.vwo.event_dispatcher.dispatch_events = mock.MagicMock()
            self.vwo.push({"tag_key_1": "tag_value_1"}, "12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)
            self.vwo.push({"tag_key_1": "tag_value_1", "tag_key_2": "tag_value_2", "tag_key_3": "tag_value_3"}, "12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 4)
            mock_event_dispatcher_dispatch.reset_mock()
            self.vwo.event_dispatcher.dispatch_events.assert_not_called()

    def test_push_with_custom_dimension_map_and_event_arch_and_event_batching(self):
        self.set_up("DUMMY_SETTINGS_FILE")
        event_arch_settings_file = SETTINGS_FILES.get("DUMMY_SETTINGS_FILE").copy()
        event_arch_settings_file["isEventArchEnabled"] = True

        self.vwo = vwo.launch(
            json.dumps(event_arch_settings_file),
            is_development_mode=True,
            log_level=TEST_LOG_LEVEL,
            batch_events={"events_per_request": 5, "request_time_interval": 1},
        )

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            self.vwo.event_dispatcher.dispatch_events = mock.MagicMock()
            self.vwo.push(custom_dimension_map={"tag_key_1": "tag_value_1"}, user_id="12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)
            self.vwo.push(
                custom_dimension_map={
                    "tag_key_1": "tag_value_1",
                    "tag_key_2": "tag_value_2",
                    "tag_key_3": "tag_value_3",
                },
                user_id="12345",
            )
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 4)
            mock_event_dispatcher_dispatch.reset_mock()
            self.vwo.event_dispatcher.dispatch_events.assert_not_called()

    def test_push_with_event_arch_and_event_batching_disabled(self):
        self.set_up("DUMMY_SETTINGS_FILE")
        event_arch_settings_file = SETTINGS_FILES.get("DUMMY_SETTINGS_FILE").copy()
        event_arch_settings_file["isEventArchEnabled"] = True
        self.vwo = vwo.launch(json.dumps(event_arch_settings_file), is_development_mode=True, log_level=TEST_LOG_LEVEL)

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch_events", return_value=None
        ) as mock_event_dispatcher_dispatch:
            self.vwo.event_dispatcher.dispatch = mock.MagicMock()
            self.vwo.push("browser", "a", "12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)
            self.vwo.push("browser", "a", "12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 2)
            mock_event_dispatcher_dispatch.reset_mock()
            self.vwo.event_dispatcher.dispatch.assert_not_called()

    def test_push_with_event_arch_and_event_batching_enabled(self):
        self.set_up("DUMMY_SETTINGS_FILE")
        event_arch_settings_file = SETTINGS_FILES.get("DUMMY_SETTINGS_FILE").copy()
        event_arch_settings_file["isEventArchEnabled"] = True
        self.vwo = vwo.launch(
            json.dumps(event_arch_settings_file),
            is_development_mode=True,
            log_level=TEST_LOG_LEVEL,
            batch_events={"events_per_request": 5, "request_time_interval": 1},
        )

        with mock.patch(
            "vwo.event.event_dispatcher.EventDispatcher.dispatch", return_value=None
        ) as mock_event_dispatcher_dispatch:
            self.vwo.event_dispatcher.dispatch_events = mock.MagicMock()
            self.vwo.push("browser", "a", "12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 1)
            self.vwo.push("browser", "a", "12345")
            self.assertIs(mock_event_dispatcher_dispatch.call_count, 2)
            mock_event_dispatcher_dispatch.reset_mock()
            self.vwo.event_dispatcher.dispatch_events.assert_not_called()

    def test_push_longer_than_255_value_false(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("DUMMY_SETTINGS_FILE")), log_level=TEST_LOG_LEVEL, is_development_mode=True
        )
        self.assertIs(False, vwo_instance.push("browser", "a" * 256, "12345"))

    def test_push_exact_255_value_true(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("DUMMY_SETTINGS_FILE")), log_level=TEST_LOG_LEVEL, is_development_mode=True
        )
        self.assertIs(True, vwo_instance.push("browser", "a" * 255, "12345"))

    def test_push_longer_than_255_key_false(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("DUMMY_SETTINGS_FILE")), log_level=TEST_LOG_LEVEL, is_development_mode=True
        )
        self.assertIs(False, vwo_instance.push("a" * 256, "browser", "12345"))

    def test_push_exact_255_key_true(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("DUMMY_SETTINGS_FILE")), log_level=TEST_LOG_LEVEL, is_development_mode=True
        )
        self.assertIs(True, vwo_instance.push("a" * 255, "browser", "12345"))
